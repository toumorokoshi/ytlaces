import importlib.util
from importlib.machinery import SourceFileLoader
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

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
compute_skill_diff = sync_skills_module.compute_skill_diff
parse_action = sync_skills_module.parse_action
prompt_action = sync_skills_module.prompt_action
delete_local_skill = sync_skills_module.delete_local_skill
delete_remote_skill = sync_skills_module.delete_remote_skill
sync_skills = sync_skills_module.sync_skills
parse_args = sync_skills_module.parse_args


class TestSyncSkillsPureFunctions(unittest.TestCase):
    def test_filter_skill_names(self):
        raw = ["", "  ", ".DS_Store", ".git", "valid-skill", "another_skill  ", ".hidden"]
        self.assertEqual(filter_skill_names(raw), {"valid-skill", "another_skill"})

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

    @patch("subprocess.run")
    def test_delete_remote_skill(self, mock_run):
        delete_remote_skill("myhost", "~/.agents/skills", "skill space")
        mock_run.assert_called_once_with(
            ["ssh", "myhost", "rm -rf ~/.agents/skills/'skill space'"],
            check=True,
        )

    @patch("subprocess.run")
    @patch("sync_skills_module.get_remote_skills")
    @patch("sync_skills_module.get_local_skills")
    @patch("sync_skills_module.delete_local_skill")
    @patch("sync_skills_module.delete_remote_skill")
    def test_sync_skills_workflow(
        self,
        mock_delete_remote,
        mock_delete_local,
        mock_local_skills,
        mock_remote_skills,
        mock_run,
    ):
        mock_local_skills.return_value = {"common", "local-only"}
        mock_remote_skills.return_value = {"common", "remote-only"}

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


if __name__ == "__main__":
    unittest.main()
