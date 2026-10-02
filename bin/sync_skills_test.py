import importlib.util
from importlib.machinery import SourceFileLoader
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, call, patch

# Load sync-skills as a module dynamically
script_path = (
    Path(__file__).parent.parent
    / "configs"
    / "standard"
    / "files-home"
    / ".ytlaces"
    / "cookbook"
    / "sync-skills"
)
loader = SourceFileLoader("sync_skills_module", str(script_path))
spec = importlib.util.spec_from_loader("sync_skills_module", loader)
sync_skills_module = importlib.util.module_from_spec(spec)
sys.modules["sync_skills_module"] = sync_skills_module
loader.exec_module(sync_skills_module)

filter_skill_names = sync_skills_module.filter_skill_names
filter_paths = sync_skills_module.filter_paths
is_subpath_of_any = sync_skills_module.is_subpath_of_any
parse_remote_find_output = sync_skills_module.parse_remote_find_output
compute_skill_diff = sync_skills_module.compute_skill_diff
parse_action = sync_skills_module.parse_action
prompt_action = sync_skills_module.prompt_action
delete_local_skill = sync_skills_module.delete_local_skill
delete_remote_skill = sync_skills_module.delete_remote_skill
delete_local_file = sync_skills_module.delete_local_file
delete_remote_file = sync_skills_module.delete_remote_file
delete_local_dir = sync_skills_module.delete_local_dir
delete_remote_dir = sync_skills_module.delete_remote_dir
get_local_entries = sync_skills_module.get_local_entries
sync_skills = sync_skills_module.sync_skills
parse_args = sync_skills_module.parse_args


class TestSyncSkillsPureFunctions(unittest.TestCase):
    def test_filter_skill_names(self):
        raw = ["", "  ", ".DS_Store", ".git", "valid-skill", "another_skill  ", ".hidden"]
        self.assertEqual(filter_skill_names(raw), {"valid-skill", "another_skill"})

    def test_filter_paths(self):
        raw = [
            "",
            "  ",
            "./.DS_Store",
            ".git/config",
            "skill1/.git/HEAD",
            "./valid-skill",
            "skill2/scripts/run.py",
            "skill3/.hidden/file.txt",
            "./root_file.md  ",
        ]
        self.assertEqual(
            filter_paths(raw),
            {"valid-skill", "skill2/scripts/run.py", "root_file.md"},
        )

    def test_is_subpath_of_any(self):
        parents = ["skill1", "skill2/sub"]
        self.assertTrue(is_subpath_of_any("skill1", parents))
        self.assertTrue(is_subpath_of_any("skill1/SKILL.md", parents))
        self.assertTrue(is_subpath_of_any("skill1/sub/run.py", parents))
        self.assertTrue(is_subpath_of_any("skill2/sub/file.txt", parents))
        self.assertFalse(is_subpath_of_any("skill1-alt", parents))
        self.assertFalse(is_subpath_of_any("skill1-alt/SKILL.md", parents))
        self.assertFalse(is_subpath_of_any("skill2", parents))
        self.assertFalse(is_subpath_of_any("other", parents))

    def test_parse_remote_find_output(self):
        output = (
            "./skill1\n"
            "./skill1/scripts\n"
            "./.git\n"
            "---\n"
            "./skill1/SKILL.md\n"
            "./skill1/scripts/tool.py\n"
            "./.DS_Store\n"
            "./top.txt\n"
        )
        dirs, files = parse_remote_find_output(output)
        self.assertEqual(dirs, {"skill1", "skill1/scripts"})
        self.assertEqual(files, {"skill1/SKILL.md", "skill1/scripts/tool.py", "top.txt"})

    def test_compute_skill_diff(self):
        local = {"a", "b", "c"}
        remote = {"b", "c", "d"}
        local_only, remote_only = compute_skill_diff(local, remote)
        self.assertEqual(local_only, ["a"])
        self.assertEqual(remote_only, ["d"])

    def test_parse_action(self):
        self.assertEqual(parse_action("c"), "copy")
        self.assertEqual(parse_action("C"), "copy")
        self.assertEqual(parse_action("copy"), "copy")
        self.assertEqual(parse_action("COPY"), "copy")
        self.assertEqual(parse_action("d"), "delete")
        self.assertEqual(parse_action("D"), "delete")
        self.assertEqual(parse_action("delete"), "delete")
        self.assertEqual(parse_action("DELETE"), "delete")
        self.assertEqual(parse_action(""), "")
        self.assertEqual(parse_action("invalid"), "")

    def test_parse_args(self):
        args = parse_args(["my-host"])
        self.assertEqual(args.remote_host, "my-host")

        with self.assertRaises(SystemExit):
            with patch("sys.stderr"):
                parse_args([])


class TestSyncSkillsStateFunctions(unittest.TestCase):
    def test_prompt_action_valid(self):
        self.assertEqual(prompt_action("skill1", "cruise", input_func=lambda _: "c"), "copy")
        self.assertEqual(prompt_action("skill2", "cruise", input_func=lambda _: "d"), "delete")

    def test_prompt_action_item_type(self):
        prompts = []

        def capture_input(prompt):
            prompts.append(prompt)
            return "c"

        prompt_action("skill1/file.py", "cruise", input_func=capture_input, item_type="File")
        self.assertEqual(
            prompts[0],
            "File 'skill1/file.py' is missing on cruise. [c]opy or [d]elete? ",
        )

    def test_prompt_action_retry_on_invalid(self):
        inputs = iter(["what", "invalid", "c"])
        self.assertEqual(prompt_action("skill1", "cruise", input_func=lambda _: next(inputs)), "copy")

    def test_delete_local_skill(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "my-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("test")
            self.assertTrue(skill_dir.exists())

            delete_local_skill(skill_dir)
            self.assertFalse(skill_dir.exists())

    def test_delete_local_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.txt"
            file_path.write_text("test")
            self.assertTrue(file_path.exists())

            delete_local_file(file_path, rel_path="test.txt")
            self.assertFalse(file_path.exists())

    @patch("subprocess.run")
    def test_delete_remote_skill(self, mock_run):
        delete_remote_skill("myhost", "~/.agents/skills", "skill space")
        mock_run.assert_called_once_with(
            ["ssh", "myhost", "rm -rf ~/.agents/skills/'skill space'"],
            check=True,
        )

    @patch("subprocess.run")
    def test_delete_remote_file(self, mock_run):
        delete_remote_file("myhost", "~/.agents/skills", "skill1/file space.py")
        mock_run.assert_called_once_with(
            ["ssh", "myhost", "rm -rf ~/.agents/skills/'skill1/file space.py'"],
            check=True,
        )

    def test_get_local_entries(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            (base / "skill1" / "scripts").mkdir(parents=True)
            (base / "skill1" / "SKILL.md").write_text("test")
            (base / "skill1" / "scripts" / "tool.py").write_text("test")
            (base / "skill1" / ".git").mkdir()
            (base / "skill1" / ".git" / "config").write_text("test")
            (base / "skill1" / ".DS_Store").write_text("test")
            (base / "standalone.md").write_text("test")

            dirs, files = get_local_entries(base)
            self.assertEqual(dirs, {"skill1", "skill1/scripts"})
            self.assertEqual(files, {"skill1/SKILL.md", "skill1/scripts/tool.py", "standalone.md"})

    @patch("subprocess.run")
    @patch("sync_skills_module.get_remote_entries")
    @patch("sync_skills_module.get_local_entries")
    @patch("sync_skills_module.delete_local_skill")
    @patch("sync_skills_module.delete_remote_skill")
    def test_sync_skills_workflow_skills(
        self,
        mock_delete_remote,
        mock_delete_local,
        mock_local_entries,
        mock_remote_entries,
        mock_run,
    ):
        mock_local_entries.return_value = ({"common", "local-only"}, set())
        mock_remote_entries.return_value = ({"common", "remote-only"}, set())

        # For local-only: choose 'delete'
        # For remote-only: choose 'copy'
        responses = iter(["d", "c"])

        with tempfile.TemporaryDirectory() as temp_dir:
            local_dir = Path(temp_dir) / "skills"
            sync_skills(
                remote_host="myhost",
                local_dir=local_dir,
                remote_dir="~/.agents/skills",
                input_func=lambda _: next(responses),
            )

            # Local-only was chosen to delete
            mock_delete_local.assert_called_once_with(local_dir / "local-only")
            # Remote-only was chosen to copy (not deleted)
            mock_delete_remote.assert_not_called()

            # Verify rsync was run in both directions
            rsync_calls = [
                call_args[0][0]
                for call_args in mock_run.call_args_list
                if call_args[0][0][0] == "rsync"
            ]
            self.assertEqual(len(rsync_calls), 2)
            # Local -> Remote
            self.assertEqual(
                rsync_calls[0],
                ["rsync", "-avzuh", "--progress", f"{local_dir}/", "myhost:~/.agents/skills/"],
            )
            # Remote -> Local
            self.assertEqual(
                rsync_calls[1],
                ["rsync", "-avzuh", "--progress", "myhost:~/.agents/skills/", f"{local_dir}/"],
            )

    @patch("subprocess.run")
    @patch("sync_skills_module.get_remote_entries")
    @patch("sync_skills_module.get_local_entries")
    @patch("sync_skills_module.delete_local_file")
    @patch("sync_skills_module.delete_remote_file")
    def test_sync_skills_workflow_files(
        self,
        mock_delete_remote_file,
        mock_delete_local_file,
        mock_local_entries,
        mock_remote_entries,
        mock_run,
    ):
        # Both sides have 'common' directory
        # Local has an extra file 'common/local_file.txt' and root file 'root.txt'
        # Remote has an extra file 'common/remote_file.txt'
        mock_local_entries.return_value = (
            {"common"},
            {"common/SKILL.md", "common/local_file.txt", "root.txt"},
        )
        mock_remote_entries.return_value = (
            {"common"},
            {"common/SKILL.md", "common/remote_file.txt"},
        )

        prompts = []

        def capture_input(prompt):
            prompts.append(prompt)
            if "local_file.txt" in prompt:
                return "d"
            if "root.txt" in prompt:
                return "c"
            if "remote_file.txt" in prompt:
                return "d"
            return "c"

        with tempfile.TemporaryDirectory() as temp_dir:
            local_dir = Path(temp_dir) / "skills"
            sync_skills(
                remote_host="myhost",
                local_dir=local_dir,
                remote_dir="~/.agents/skills",
                input_func=capture_input,
            )

            # Prompts should be generated for each individual file
            self.assertEqual(len(prompts), 3)
            self.assertIn("File 'common/local_file.txt' is missing on myhost.", prompts[0])
            self.assertIn("File 'root.txt' is missing on myhost.", prompts[1])
            self.assertIn("File 'common/remote_file.txt' is missing on local.", prompts[2])

            # Local file was chosen to delete
            mock_delete_local_file.assert_called_once_with(
                local_dir / "common/local_file.txt",
                rel_path="common/local_file.txt",
            )
            # Remote file was chosen to delete
            mock_delete_remote_file.assert_called_once_with(
                "myhost",
                "~/.agents/skills",
                "common/remote_file.txt",
            )

    @patch("subprocess.run")
    @patch("sync_skills_module.get_remote_entries")
    @patch("sync_skills_module.get_local_entries")
    @patch("sync_skills_module.delete_local_skill")
    def test_sync_skills_workflow_skip_children_when_dir_handled(
        self,
        mock_delete_local_skill,
        mock_local_entries,
        mock_remote_entries,
        mock_run,
    ):
        # Local has a whole new skill with nested dirs and files
        mock_local_entries.return_value = (
            {"new-skill", "new-skill/scripts"},
            {"new-skill/SKILL.md", "new-skill/scripts/tool.py"},
        )
        mock_remote_entries.return_value = (set(), set())

        prompts = []

        def capture_input(prompt):
            prompts.append(prompt)
            return "d"

        with tempfile.TemporaryDirectory() as temp_dir:
            local_dir = Path(temp_dir) / "skills"
            sync_skills(
                remote_host="myhost",
                local_dir=local_dir,
                remote_dir="~/.agents/skills",
                input_func=capture_input,
            )

            # Only 1 prompt for the top-level skill directory
            self.assertEqual(len(prompts), 1)
            self.assertIn("Skill 'new-skill' is missing on myhost.", prompts[0])
            mock_delete_local_skill.assert_called_once_with(local_dir / "new-skill")


if __name__ == "__main__":
    unittest.main()
