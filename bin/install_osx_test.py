import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
from pathlib import Path
import importlib.util

# Ensure yaml mock is available if pyyaml is not installed
if "yaml" not in sys.modules:
    sys.modules["yaml"] = MagicMock()

file_path = Path(__file__).parent / "install-osx.py"
spec = importlib.util.spec_from_file_location("install_osx", file_path)
install_osx = importlib.util.module_from_spec(spec)
sys.modules["install_osx"] = install_osx
spec.loader.exec_module(install_osx)

Manifest = install_osx.Manifest
Binary = install_osx.Binary
BinaryManifestEntry = install_osx.BinaryManifestEntry


class TestManifest(unittest.TestCase):
    def test_from_dict(self):
        data = {"binaries": {"foo": {"url": "http://example.com/foo"}}}
        manifest = Manifest.from_dict(data)
        self.assertEqual(manifest.binaries["foo"].url, "http://example.com/foo")

    def test_to_dict(self):
        manifest = Manifest(
            binaries={"foo": BinaryManifestEntry(url="http://example.com/foo")}
        )
        self.assertEqual(
            manifest.to_dict(), {"binaries": {"foo": {"url": "http://example.com/foo"}}}
        )

    def test_empty(self):
        manifest = Manifest()
        self.assertEqual(manifest.binaries, {})

    @patch(
        "install_osx.open",
        new_callable=mock_open,
        read_data="binaries:\n  foo:\n    url: http://example.com/foo",
    )
    @patch("install_osx.yaml.safe_load")
    def test_load_manifest(self, mock_yaml, mock_file):
        mock_yaml.side_effect = lambda f: {
            "binaries": {"foo": {"url": "http://example.com/foo"}}
        }

        mock_path = MagicMock()
        mock_path.exists.return_value = True

        manifest = install_osx.load_manifest(mock_path)
        self.assertEqual(manifest.binaries["foo"].url, "http://example.com/foo")

    @patch("install_osx.open", new_callable=mock_open)
    @patch("install_osx.yaml.dump")
    def test_save_manifest(self, mock_yaml, mock_file):
        manifest = Manifest(
            binaries={"foo": BinaryManifestEntry(url="http://example.com/foo")}
        )
        install_osx.save_manifest(Path("/tmp/manifest.yaml"), manifest)
        mock_yaml.assert_called_once()
        self.assertEqual(
            mock_yaml.call_args[0][0],
            {"binaries": {"foo": {"url": "http://example.com/foo"}}},
        )


class TestBinary(unittest.TestCase):
    @patch("install_osx.platform.machine", return_value="arm64")
    def test_from_dict_with_arch_substitution(self, mock_machine):
        data = {
            "name": "tome",
            "url": "https://example.com/download/tome-macOS-{arch}.tar.gz",
            "format": "tar.gz",
            "sha256": {
                "arm64": "hash_arm",
                "x86_64": "hash_x86",
            },
        }
        b = Binary.from_dict(data)
        self.assertEqual(b.name, "tome")
        self.assertEqual(
            b.url, "https://example.com/download/tome-macOS-arm64.tar.gz"
        )
        self.assertEqual(b.format, "tar.gz")
        self.assertEqual(b.sha256, "hash_arm")

    @patch("install_osx.platform.machine", return_value="x86_64")
    def test_from_dict_plain_url(self, mock_machine):
        data = {
            "name": "plain",
            "url": "https://example.com/plain",
            "sha256": "single_hash",
        }
        b = Binary.from_dict(data)
        self.assertEqual(b.name, "plain")
        self.assertEqual(b.url, "https://example.com/plain")
        self.assertEqual(b.sha256, "single_hash")
        self.assertIsNone(b.format)


class TestInstallBinaries(unittest.TestCase):
    def setUp(self):
        self.mock_logger = patch("install_osx.LOGGER").start()
        self.mock_pwd = patch("install_osx.pwd").start()
        self.mock_pwd.getpwnam.return_value.pw_uid = 1000

        self.mock_os = patch("install_osx.os").start()
        self.mock_os.path.exists.return_value = False

        self.mock_download = patch("install_osx._download_and_install_binary").start()
        self.mock_download.return_value = True

        self.mock_tar_install = patch("install_osx._install_tar_gz_binary").start()
        self.mock_tar_install.return_value = True

        self.mock_load_manifest = patch("install_osx.load_manifest").start()
        self.mock_save_manifest = patch("install_osx.save_manifest").start()

        self.files_home_dir = Path("/tmp/files-home")
        self.binaries = [
            Binary(name="foo", url="http://example.com/foo"),
            Binary(name="bar", url="http://example.com/bar", format="tar.gz"),
        ]

    def tearDown(self):
        patch.stopall()

    def test_install_new_binaries(self):
        self.mock_load_manifest.return_value = Manifest()

        install_osx._install_binaries("testuser", self.files_home_dir, self.binaries)

        self.mock_download.assert_called_with(
            self.binaries[0], str(self.files_home_dir / "bin/foo"), 1000
        )
        self.mock_tar_install.assert_called_with(
            self.binaries[1], self.files_home_dir / "bin", 1000
        )

        self.mock_save_manifest.assert_called_once()
        saved_manifest = self.mock_save_manifest.call_args[0][1]
        self.assertEqual(saved_manifest.binaries["foo"].url, "http://example.com/foo")
        self.assertEqual(saved_manifest.binaries["bar"].url, "http://example.com/bar")

    def test_skip_existing_manifest_match_file_exists(self):
        manifest = Manifest(
            binaries={"foo": BinaryManifestEntry(url="http://example.com/foo")}
        )
        self.mock_load_manifest.return_value = manifest

        def side_effect(path):
            if str(path).endswith("foo"):
                return True
            return False

        self.mock_os.path.exists.side_effect = side_effect

        install_osx._install_binaries(
            "testuser", self.files_home_dir, [self.binaries[0]]
        )

        self.mock_download.assert_not_called()
        self.mock_save_manifest.assert_not_called()

    def test_reinstall_if_url_changed(self):
        manifest = Manifest(
            binaries={"foo": BinaryManifestEntry(url="http://example.com/OLD_URL")}
        )
        self.mock_load_manifest.return_value = manifest

        def side_effect(path):
            if str(path).endswith("foo"):
                return True
            return False

        self.mock_os.path.exists.side_effect = side_effect

        install_osx._install_binaries(
            "testuser", self.files_home_dir, [self.binaries[0]]
        )

        self.mock_download.assert_called_once()
        self.mock_save_manifest.assert_called_once()
        saved_manifest = self.mock_save_manifest.call_args[0][1]
        self.assertEqual(saved_manifest.binaries["foo"].url, "http://example.com/foo")

    def test_reinstall_if_file_missing_even_if_manifest_match(self):
        manifest = Manifest(
            binaries={"foo": BinaryManifestEntry(url="http://example.com/foo")}
        )
        self.mock_load_manifest.return_value = manifest

        self.mock_os.path.exists.return_value = False

        install_osx._install_binaries(
            "testuser", self.files_home_dir, [self.binaries[0]]
        )

        self.mock_download.assert_called_once()
        self.mock_save_manifest.assert_called_once()


if __name__ == "__main__":
    unittest.main()
