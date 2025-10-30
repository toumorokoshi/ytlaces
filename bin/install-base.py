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
import tarfile
import tempfile
import hashlib

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
class Binary:
    name: str
    url: str
    sha256: Optional[str] = None
    format: Optional[str] = None

    def from_dict(data: dict) -> "Binary":
        return Binary(
            name=data["name"],
            url=data["url"],
            sha256=data.get("sha256"),
            format=data.get("format"),
        )

    def __str__(self):
        return self.name


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
class SystemdConfig:
    user_services: Set[str] = field(default_factory=set)

    @staticmethod
    def from_dict(data: dict) -> "SystemdConfig":
        return SystemdConfig(
            user_services=set(data.get("user_services", [])),
        )


@dataclass
class Config:
    binaries: Optional[list[Binary]] = field(default_factory=None)
    packages: Optional[list[Package]] = field(default_factory=None)
    rust: Optional[RustConfig] = field(default=None)
    systemd: Optional[SystemdConfig] = field(default=None)

    def from_dict(data: dict) -> "Config":
        packages = None
        if "packages" in data:
            packages = (
                [Package.from_dict(pkg) for pkg in data.get("packages", [])]
                if data.get("packages")
                else None
            )
        rust = RustConfig.from_dict(data["rust"]) if data.get("rust") else None
        if "binaries" in data:
            binaries = [Binary.from_dict(bin) for bin in data.get("binaries", [])]
        else:
            binaries = None
        systemd = (
            SystemdConfig.from_dict(data["systemd"]) if data.get("systemd") else None
        )
        return Config(packages=packages, rust=rust, binaries=binaries, systemd=systemd)


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
    target_home_dir = Path(f"/home/{username}")
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
    if config.binaries:
        _install_binaries(username, target_home_dir, config.binaries)
    if files_dir.exists():
        _recursive_copy_files(str(files_dir), "/")
    if files_home_dir.exists():
        _recursive_copy_files(str(files_home_dir), target_home_dir, user=username)
    if config.systemd:
        _setup_systemd_services(username, config.systemd)


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


def _install_binaries(username: str, files_home_dir: Path, binaries: list[Binary]):
    LOGGER.info("Installing binaries...")
    binary_root = files_home_dir / "bin"
    if not binary_root.exists():
        os.makedirs(binary_root)
    for binary in binaries:
        target_path = f"{binary_root}/{binary.name}"
        uid = pwd.getpwnam(username).pw_uid

        if (binary.format or "").lower() == "tar.gz":
            _install_tar_gz_binary(binary, binary_root, uid)
        else:
            _download_and_install_binary(binary, target_path, uid)


def _download_and_install_binary(binary: Binary, target_path: str, uid: int):
    # Default behavior: download a single binary file
    if os.path.exists(target_path):
        if not binary.sha256:
            LOGGER.info(
                f"Binary {binary.name} already installed, no required sha256 specified"
            )
            return
        actual_sha256 = os.popen(f"sha256sum {target_path}").read().split()[0]
        if actual_sha256 == binary.sha256:
            LOGGER.info(
                f"Binary {binary.name} already installed with SHA256 {binary.sha256}."
            )
            return
    LOGGER.info(f"Downloading {binary.name} from {binary.url} to {target_path}")
    os.system(f"curl -L {binary.url} -o {target_path}")
    os.system(f"chmod +x {target_path}")
    os.chown(target_path, uid, -1)
    LOGGER.info(f"Installed binary: {binary.name}")


def _safe_tar_members(tar: tarfile.TarFile):
    """Yield members that are safe to extract (no absolute paths, no path traversal)."""
    for member in tar.getmembers():
        member_path = member.name
        # Reject absolute paths and up-level references
        if member_path.startswith("/"):
            LOGGER.warning(f"Skipping absolute path in tar: {member_path}")
            continue
        normalized = os.path.normpath(member_path)
        if normalized.startswith(".."):
            LOGGER.warning(f"Skipping unsafe path in tar: {member_path}")
            continue
        yield member


def _install_tar_gz_binary(binary: Binary, binary_root: Path, uid: int) -> bool:
    """Download and extract a tar.gz binary into the given bin directory.

    Returns True on success, False on failure.
    """
    LOGGER.info(f"Downloading tar.gz {binary.name} from {binary.url}")
    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp_file:
        tmp_path = tmp_file.name
    try:
        os.system(f"curl -L {binary.url} -o {tmp_path}")

        # If sha256 is provided, verify the archive before extraction
        if binary.sha256:
            sha256_hash = hashlib.sha256()
            with open(tmp_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256_hash.update(chunk)
            actual_sha = sha256_hash.hexdigest()
            if actual_sha != binary.sha256:
                LOGGER.error(
                    f"SHA256 mismatch for {binary.name}: expected {binary.sha256}, got {actual_sha}. Skipping extraction."
                )
                return False

        # Extract safely into the bin directory
        with tarfile.open(tmp_path, "r:gz") as tar:
            members = _safe_tar_members(tar)
            tar.extractall(path=binary_root, members=members)

        # Ensure ownership and executability for extracted files
        with tarfile.open(tmp_path, "r:gz") as tar:
            for m in tar.getmembers():
                if m.isdir():
                    continue
                dest_file = os.path.join(binary_root, m.name)
                # Normalize any leading './'
                dest_file = os.path.normpath(dest_file)
                if os.path.exists(dest_file):
                    try:
                        os.chown(dest_file, uid, -1)
                    except PermissionError:
                        LOGGER.warning(f"Failed to chown {dest_file}")
                    # Make files executable to match previous behavior
                    try:
                        st = os.stat(dest_file)
                        os.chmod(dest_file, st.st_mode | 0o111)
                    except PermissionError:
                        LOGGER.warning(f"Failed to chmod +x {dest_file}")

        LOGGER.info(f"Extracted archive for: {binary.name} -> {binary_root}")
        return True
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


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


def _setup_systemd_services(username: str, systemd_config: SystemdConfig):
    """Enable and start systemd user services."""
    if not systemd_config.user_services:
        return

    LOGGER.info("Setting up systemd user services...")

    for service_name in systemd_config.user_services:
        LOGGER.info(f"  Setting up systemd user service: {service_name}")

        # Reload systemd user daemon to pick up new services
        os.system(f"systemctl --user -M {username}@ daemon-reload")

        # Enable the service
        LOGGER.info(f"  Enabling {service_name}")
        os.system(f"systemctl --user -M {username}@ enable {service_name}")

        # Start the service
        LOGGER.info(f"  Starting {service_name}")
        os.system(f"systemctl --user -M {username}@ start {service_name}")

        # resStart the service
        LOGGER.info(f"  Restarting {service_name}")
        os.system(f"systemctl --user -M {username}@ restart {service_name}")


def _run_as_user(username: str, command: str):
    full_command = f'su - {username} -c "{command}"'
    print(f"running {full_command}")
    result = os.system(full_command)
    if result != 0:
        LOGGER.error(f"Command failed: {command}")
    else:
        LOGGER.info(f"Successfully ran command as {username}: {command}")


if __name__ == "__main__":
    main()
