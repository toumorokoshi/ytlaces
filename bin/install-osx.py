#!/usr/bin/env python3
# install base files and executables required for all host configurations on macOS.
import logging
import os
import pwd
import shutil
import sys
from pathlib import Path
import argparse
import yaml
from dataclasses import dataclass, field
from typing import Set, Optional

LOGGER = logging.getLogger("install-osx")


@dataclass
class RustConfig:
    packages: Set[str] = field(default_factory=set)
    binstall_packages: Set[str] = field(default_factory=set)

    @staticmethod
    def from_dict(data: dict) -> "RustConfig":
        return RustConfig(
            packages=set(data.get("packages", [])),
            binstall_packages=set(data.get("binstall_packages", [])),
        )


@dataclass
class Binary:
    name: str
    url: str
    sha256: Optional[str] = None

    def from_dict(data: dict) -> "Binary":
        return Binary(
            name=data["name"],
            url=data["url"],
            sha256=data.get("sha256"),
        )

    def __str__(self):
        return self.name


@dataclass
class BrewPackage:
    name: str
    tap: Optional[str] = None

    def from_dict(data: dict) -> "BrewPackage":
        return BrewPackage(
            name=data["name"],
            tap=data.get("tap"),
        )

    def __str__(self):
        return self.name


@dataclass
class MacApp:
    name: str
    url: str
    format: str  # "zip" or "dmg"
    app_name: str

    @staticmethod
    def from_dict(data: dict) -> "MacApp":
        return MacApp(
            name=data["name"],
            url=data["url"],
            format=data["format"],
            app_name=data["app_name"],
        )


@dataclass
class Config:
    binaries: Optional[list[Binary]] = field(default_factory=None)
    brew_packages: Optional[list[BrewPackage]] = field(default_factory=None)
    rust: Optional[RustConfig] = field(default=None)
    mac_apps: Optional[list[MacApp]] = field(default_factory=None)
    post_install_messages: Optional[list[str]] = field(default_factory=list)

    def from_dict(data: dict) -> "Config":
        brew_packages = None
        if "brew_packages" in data:
            brew_packages = (
                [BrewPackage.from_dict(pkg) for pkg in data.get("brew_packages", [])]
                if data.get("brew_packages")
                else None
            )
        rust = RustConfig.from_dict(data["rust"]) if data.get("rust") else None
        if "binaries" in data:
            binaries = [Binary.from_dict(bin) for bin in data.get("binaries", [])]
        else:
            binaries = None
        mac_apps = None
        if "mac_apps" in data:
            mac_apps = (
                [MacApp.from_dict(app) for app in data.get("mac_apps", [])]
                if data.get("mac_apps")
                else None
            )
        post_install_messages = data.get("post_install_messages", [])
        return Config(
            brew_packages=brew_packages,
            rust=rust,
            binaries=binaries,
            mac_apps=mac_apps,
            post_install_messages=post_install_messages,
        )


def load_config(config_path) -> Config:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file {config_path} does not exist.")
    with open(config_path, "r") as f:
        raw = yaml.safe_load(f)
    return Config.from_dict(raw)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Install base files and executables required for all host configurations on macOS."
    )
    parser.add_argument(
        "root_dir",
        type=Path,
        help="Root directory containing files, files-home, and config.yaml",
    )
    parser.add_argument(
        "username", type=str, help="Target username for home directory operations"
    )
    args = parser.parse_args(argv)

    root_dir = args.root_dir.resolve()
    username = args.username

    files_dir = root_dir / "files"
    files_home_dir = root_dir / "files-home"
    target_home_dir = Path(f"/Users/{username}")
    config_path = root_dir / "config.yaml"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if not config_path.exists():
        LOGGER.critical(f"Config file {config_path} does not exist.")
        return

    config = load_config(config_path)

    # Check if Homebrew is installed
    if not _check_homebrew_installed():
        LOGGER.critical("Homebrew is not installed. Please install Homebrew first.")
        return

    if config.brew_packages:
        _install_brew_packages(config.brew_packages)
    if config.rust:
        _install_rust(username, config.rust)
    if config.binaries:
        _install_binaries(username, target_home_dir, config.binaries)
    if files_dir.exists():
        _recursive_copy_files(str(files_dir), "/")
    if files_home_dir.exists():
        _recursive_copy_files(str(files_home_dir), target_home_dir, user=username)
    if config.mac_apps:
        _install_mac_apps(username, root_dir, config.mac_apps)

    if config.post_install_messages:
        print("\n" + "="*80)
        for msg in config.post_install_messages:
            print(msg)
        print("="*80 + "\n")


def _check_homebrew_installed() -> bool:
    """Check if Homebrew is installed."""
    return os.system("which brew > /dev/null 2>&1") == 0


def _add_taps(taps: set[str]):
    """Add Homebrew taps."""
    LOGGER.info("Adding Homebrew taps...")
    for tap in taps:
        LOGGER.info(f"Adding tap: {tap}")
        os.system(f"brew tap {tap}")
    LOGGER.info("Updated taps")


def _install_brew_packages(packages: list[BrewPackage]):
    """Install Homebrew packages."""
    taps = {p.tap for p in packages if p.tap}
    if taps:
        _add_taps(taps)

    package_names = {pkg.name for pkg in packages}
    LOGGER.info("Installing Homebrew packages...")
    os.system(f"brew install {' '.join(package_names)}")
    LOGGER.info(f"Installed packages: {', '.join(package_names)}")


def _install_rust(username: str, rust_config: RustConfig):
    """Install Rust packages using cargo."""
    LOGGER.info("Installing and updating Rust...")
    _run_as_user(username, "rustup default stable")
    rust_packages = rust_config.packages
    if len(rust_config.binstall_packages) > 0:
        rust_packages.add("cargo-binstall")
    if rust_packages:
        _run_as_user(username, f"cargo install {' '.join(rust_packages)}")
    if rust_config.binstall_packages:
        _run_as_user(
            username, f"cargo binstall -y {' '.join(rust_config.binstall_packages)}"
        )


def _install_binaries(username: str, files_home_dir: Path, binaries: list[Binary]):
    """Install binary files."""
    LOGGER.info("Installing binaries...")
    binary_root = files_home_dir / "bin"
    os.makedirs(binary_root, exist_ok=True)

    for binary in binaries:
        target_path = f"{binary_root}/{binary.name}"
        if os.path.exists(target_path):
            if not binary.sha256:
                LOGGER.info(
                    f"Binary {binary.name} already installed, no required sha256 specified"
                )
                continue
            actual_sha256 = os.popen(f"shasum -a 256 {target_path}").read().split()[0]
            if actual_sha256 == binary.sha256:
                LOGGER.info(
                    f"Binary {binary.name} already installed with SHA256 {binary.sha256}."
                )
                continue
        LOGGER.info(f"Downloading {binary.name} from {binary.url} to {target_path}")
        os.system(f"curl -L {binary.url} -o {target_path}")
        os.system(f"chmod +x {target_path}")
        try:
            uid = pwd.getpwnam(username).pw_uid
            os.chown(target_path, uid, -1)
        except KeyError:
            LOGGER.warning(f"User {username} not found, skipping ownership change")
        LOGGER.info(f"Installed binary: {binary.name}")


def _install_mac_apps(username: str, root_dir: Path, apps: list[MacApp]):
    """Download and install macOS Applications (.zip or .dmg) to /Applications/."""
    LOGGER.info("Installing macOS Applications...")
    target_apps_dir = Path("/Applications")

    # Create temp directory inside workspace root
    temp_dir = root_dir / "temp_downloads"

    for app in apps:
        app_target_path = target_apps_dir / app.app_name
        if app_target_path.exists():
            LOGGER.info(f"App {app.name} is already installed at {app_target_path}.")
            continue

        LOGGER.info(f"Installing {app.name}...")
        os.makedirs(temp_dir, exist_ok=True)
        archive_path = temp_dir / f"{app.name}_download.{app.format}"

        # Download
        LOGGER.info(f"Downloading {app.name} from {app.url}...")
        download_res = os.system(f"curl -L '{app.url}' -o '{archive_path}'")
        if download_res != 0:
            LOGGER.error(f"Failed to download {app.name}.")
            continue

        extracted_app_path = None
        mounted_volume = None

        try:
            if app.format == "zip":
                extracted_dir = temp_dir / f"{app.name}_extracted"
                os.makedirs(extracted_dir, exist_ok=True)
                LOGGER.info(f"Extracting {archive_path}...")
                unzip_res = os.system(f"unzip -q '{archive_path}' -d '{extracted_dir}'")
                if unzip_res == 0:
                    # Find app inside extracted dir
                    for root, dirs, _ in os.walk(extracted_dir):
                        for d in dirs:
                            if d == app.app_name:
                                extracted_app_path = Path(root) / d
                                break
                        if extracted_app_path:
                            break
            elif app.format == "dmg":
                LOGGER.info(f"Mounting {archive_path}...")
                mount_output = os.popen(f"hdiutil attach -nobrowse -readonly '{archive_path}'").read()
                for line in mount_output.splitlines():
                    if "/Volumes/" in line:
                        mounted_volume = Path(line.split("\t")[-1].strip())
                        break
                if mounted_volume:
                    # Look for the app bundle in the mounted volume
                    expected_path = mounted_volume / app.app_name
                    if expected_path.exists():
                        extracted_app_path = expected_path

            if extracted_app_path and extracted_app_path.exists():
                LOGGER.info(f"Copying {app.app_name} to {target_apps_dir}...")
                # Delete existing destination if it was partially copied or directory exists
                if app_target_path.exists():
                    shutil.rmtree(app_target_path)
                shutil.copytree(extracted_app_path, app_target_path, symlinks=True)

                # Update ownership to target user
                try:
                    uid = pwd.getpwnam(username).pw_uid
                    os.system(f"chown -R {username}:staff '{app_target_path}'")
                    LOGGER.info(f"Successfully installed {app.name} and set ownership to {username}.")
                except KeyError:
                    LOGGER.warning(f"User {username} not found, skipping ownership change for {app.name}.")
            else:
                LOGGER.error(f"Could not locate {app.app_name} in download.")

        finally:
            # Cleanup mount if any
            if mounted_volume:
                LOGGER.info(f"Unmounting {mounted_volume}...")
                os.system(f"hdiutil detach '{mounted_volume}'")

    # Cleanup temp directory
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


def _recursive_copy_files(src, dst, user=None):
    """Recursively copy files from source to destination."""
    for root, _, files in os.walk(src):
        relative_path = os.path.relpath(root, src)
        target_dir = os.path.join(dst, relative_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_dir, file)
            LOGGER.info(f"writing {target_file}")
            shutil.copy2(source_file, target_file)
            if user:
                try:
                    uid = pwd.getpwnam(user).pw_uid
                    os.chown(target_file, uid, -1)
                except KeyError:
                    LOGGER.warning(f"User {user} not found, skipping ownership change")


def _run_as_user(username: str, command: str):
    """Run a command as a specific user."""
    full_command = f'sudo -u {username} bash -c "{command}"'
    print(f"running {full_command}")
    result = os.system(full_command)
    if result != 0:
        LOGGER.error(f"Command failed: {command}")
    else:
        LOGGER.info(f"Successfully ran command as {username}: {command}")


if __name__ == "__main__":
    main()
