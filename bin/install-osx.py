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
class Config:
    binaries: Optional[list[Binary]] = field(default_factory=None)
    brew_packages: Optional[list[BrewPackage]] = field(default_factory=None)
    rust: Optional[RustConfig] = field(default=None)

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
        return Config(brew_packages=brew_packages, rust=rust, binaries=binaries)


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
