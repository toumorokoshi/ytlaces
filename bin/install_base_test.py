import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
from pathlib import Path
import importlib.util

# Import install-base.py which has a hyphen
file_path = Path(__file__).parent / "install-base.py"
spec = importlib.util.spec_from_file_location("install_base", file_path)
install_base = importlib.util.module_from_spec(spec)
sys.modules["install_base"] = install_base
spec.loader.exec_module(install_base)

Manifest = install_base.Manifest
Binary = install_base.Binary

class TestManifest(unittest.TestCase):
    def test_from_dict(self):
        data = {"binaries": {"foo": {"url": "http://example.com/foo"}}}
        manifest = Manifest.from_dict(data)
        self.assertEqual(manifest.binaries, data["binaries"])

    def test_to_dict(self):
        manifest = Manifest(binaries={"foo": {"url": "http://example.com/foo"}})
        self.assertEqual(manifest.to_dict(), {"binaries": {"foo": {"url": "http://example.com/foo"}}})

    def test_empty(self):
        manifest = Manifest()
        self.assertEqual(manifest.binaries, {})

    @patch("install_base.open", new_callable=mock_open, read_data="binaries:\n  foo:\n    url: http://example.com/foo")
    @patch("install_base.yaml.safe_load")
    def test_load_manifest(self, mock_yaml, mock_file):
        mock_yaml.side_effect = lambda f: {"binaries": {"foo": {"url": "http://example.com/foo"}}}

        mock_path = MagicMock()
        mock_path.exists.return_value = True

        manifest = install_base.load_manifest(mock_path)
        self.assertEqual(manifest.binaries["foo"]["url"], "http://example.com/foo")

    @patch("install_base.open", new_callable=mock_open)
    @patch("install_base.yaml.dump")
    def test_save_manifest(self, mock_yaml, mock_file):
        manifest = Manifest(binaries={"foo": {"url": "http://example.com/foo"}})
        install_base.save_manifest(Path("/tmp/manifest.yaml"), manifest)
        mock_yaml.assert_called_once()
        self.assertEqual(mock_yaml.call_args[0][0], {"binaries": {"foo": {"url": "http://example.com/foo"}}})

class TestInstallBinaries(unittest.TestCase):
    def setUp(self):
        self.mock_logger = patch("install_base.LOGGER").start()
        self.mock_pwd = patch("install_base.pwd").start()
        self.mock_pwd.getpwnam.return_value.pw_uid = 1000

        self.mock_os = patch("install_base.os").start()
        self.mock_os.path.exists.return_value = False

        self.mock_download = patch("install_base._download_and_install_binary").start()
        self.mock_download.return_value = True

        self.mock_tar_install = patch("install_base._install_tar_gz_binary").start()
        self.mock_tar_install.return_value = True

        self.mock_load_manifest = patch("install_base.load_manifest").start()
        self.mock_save_manifest = patch("install_base.save_manifest").start()

        self.files_home_dir = Path("/tmp/files-home")
        self.binaries = [
            Binary(name="foo", url="http://example.com/foo"),
            Binary(name="bar", url="http://example.com/bar", format="tar.gz")
        ]

    def tearDown(self):
        patch.stopall()

    def test_install_new_binaries(self):
        self.mock_load_manifest.return_value = Manifest()

        install_base._install_binaries("testuser", self.files_home_dir, self.binaries)

        self.mock_download.assert_called_with(self.binaries[0], str(self.files_home_dir / "bin/foo"), 1000)
        self.mock_tar_install.assert_called_with(self.binaries[1], self.files_home_dir / "bin", 1000)

        # Manifest should be updated and saved
        self.mock_save_manifest.assert_called_once()
        saved_manifest = self.mock_save_manifest.call_args[0][1]
        self.assertEqual(saved_manifest.binaries["foo"]["url"], "http://example.com/foo")
        self.assertEqual(saved_manifest.binaries["bar"]["url"], "http://example.com/bar")

    def test_skip_existing_manifest_match_file_exists(self):
        manifest = Manifest(binaries={"foo": {"url": "http://example.com/foo"}})
        self.mock_load_manifest.return_value = manifest

        # Determine behavior for os.path.exists
        # We need it to return True for the binary path
        def side_effect(path):
            if str(path).endswith("foo"):
                return True
            return False
        self.mock_os.path.exists.side_effect = side_effect

        install_base._install_binaries("testuser", self.files_home_dir, [self.binaries[0]])

        # Should NOT download
        self.mock_download.assert_not_called()
        # Should NOT save manifest (no changes)
        self.mock_save_manifest.assert_not_called()

    def test_reinstall_if_url_changed(self):
        manifest = Manifest(binaries={"foo": {"url": "http://example.com/OLD_URL"}})
        self.mock_load_manifest.return_value = manifest

        # File exists, but URL changed
        def side_effect(path):
            if str(path).endswith("foo"):
                return True
            return False
        self.mock_os.path.exists.side_effect = side_effect

        install_base._install_binaries("testuser", self.files_home_dir, [self.binaries[0]])

        # Should download
        self.mock_download.assert_called_once()
        self.mock_save_manifest.assert_called_once()
        saved_manifest = self.mock_save_manifest.call_args[0][1]
        self.assertEqual(saved_manifest.binaries["foo"]["url"], "http://example.com/foo")

    def test_reinstall_if_file_missing_even_if_manifest_match(self):
        manifest = Manifest(binaries={"foo": {"url": "http://example.com/foo"}})
        self.mock_load_manifest.return_value = manifest

        # File does NOT exist
        self.mock_os.path.exists.return_value = False

        install_base._install_binaries("testuser", self.files_home_dir, [self.binaries[0]])

        # Should download
        self.mock_download.assert_called_once()
        # Should save manifest (to confirm it's there? - logic says if success, update manifest.
        # Even if values are same, we assign it. And if we assign it, we might set updated=True?
        # Let's check logic:
        # if success: manifest.binaries[name] = url; manifest_updated = True
        # Yes, it updates and saves. This is fine.
        self.mock_save_manifest.assert_called_once()


if __name__ == "__main__":
    unittest.main()
