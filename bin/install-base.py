#!/usr/bin/env python3
# install base files and executables required for all host configurations.
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

LOGGER = logging.getLogger("install-base")


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
class Package:
    name: str
    ppa: Optional[str] = None

    def from_dict(data: dict) -> "Package":
        return Package(
            name=data["name"],
            ppa=data.get("ppa"),
        )

    def __str__(self):
        return f"{self.name}={self.version}" if self.version else self.name


@dataclass
class Config:
    packages: Optional[list[Package]] = field(default_factory=None)
    rust: Optional[RustConfig] = field(default=None)

    def from_dict(data: dict) -> "Config":
        packages = None
        if "packages" in data:
            packages = (
                [Package.from_dict(pkg) for pkg in data.get("packages", [])]
                if data.get("packages")
                else None
            )
        rust = RustConfig.from_dict(data["rust"]) if data.get("rust") else None
        return Config(packages=packages, rust=rust)


def load_config(config_path) -> Config:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file {config_path} does not exist.")
    with open(config_path, "r") as f:
        raw = yaml.safe_load(f)
    return Config.from_dict(raw)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Install base files and executables required for all host configurations."
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
    config_path = root_dir / "config.yaml"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if os.geteuid() != 0:
        LOGGER.critical("This script must be run as root.")
        return

    if not config_path.exists():
        LOGGER.critical(f"Config file {config_path} does not exist.")
        return

    config = load_config(config_path)

    if config.packages:
        _install_packages(config.packages)
    if config.rust:
        _install_rust(username, config.rust)
    if files_dir.exists():
        _recursive_copy_files(str(files_dir), "/")
    if files_home_dir.exists():
        _recursive_copy_files(
            str(files_home_dir), os.path.join("/home", username), user=username
        )


def _add_ppas(ppas: set[str]):
    LOGGER.info("Adding PPAs...")
    for ppa in ppas:
        os.system(f"add-apt-repository -y {ppa}")
        LOGGER.info(f"Added PPA: {ppa}")
    os.system("apt update")
    LOGGER.info("Updated package list after adding PPAs")


def _install_packages(packages: list[Package]):
    ppas = {p.ppa for p in packages if p.ppa}
    _add_ppas(ppas)
    package_names = {pkg.name for pkg in packages}
    LOGGER.info("Installing packages...")
    os.system(f"sudo apt install -y {' '.join(package_names)}")
    LOGGER.info(f"Installed packages: {', '.join(package_names)}")


def _install_rust(username: str, rust_config: RustConfig):
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


def _recursive_copy_files(src, dst, user=None):
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
                uid = pwd.getpwnam(user).pw_uid
                os.chown(target_file, uid, -1)


def _run_as_user(username: str, command: str):
    full_command = f'su - {username} -c "{command}"'
    result = os.system(full_command)
    if result != 0:
        LOGGER.error(f"Command failed: {command}")
    else:
        LOGGER.info(f"Successfully ran command as {username}: {command}")


if __name__ == "__main__":
    main()
