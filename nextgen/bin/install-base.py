#!/usr/bin/env python3
# install base files and executables required for all host configurations.
import logging
import os
import shutil
import sys
from pathlib import Path

MAIN_DIR = Path(__file__).resolve().parent.parent
FILES_DIR = os.path.join(MAIN_DIR, "files")
FILES_HOME_DIR = os.path.join(MAIN_DIR, "files-home")
LOGGER = logging.getLogger("install-base")
PPAS = {
    "ppa:fish-shell/release-4",  # fish shell
}
PACKAGES = {
    "fish",  # fish shell
    # helpful utility to visualize disk usage.
    "ncdu",
    # window manager I prefer to use
    "sway",
    # for IME support
    "fcitx5",
    "fcitx5-mozc",
}
# standard rust packages
RUST_PACKAGES = {
    "cargo-binstall",
}
# some packages recommend installation via cargo binstall
RUST_BINSTALL_PACKAGES = {
    "jj-cli",
}


def main(argv=sys.argv[1:]):
    username = argv[0]
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # Check if the script is run as root
    if os.geteuid() != 0:
        LOGGER.critical("This script must be run as root.")
        return

    # Check if the files directory exists
    if not os.path.exists(FILES_DIR):
        LOGGER.critical(f"Files directory {FILES_DIR} does not exist.")
        return

    _add_ppas(PPAS)
    _install_packages(PACKAGES)
    _install_and_update_rust(username)
    _recursive_copy_files(FILES_DIR, "/")
    _recursive_copy_files(FILES_HOME_DIR, os.path.join("/home", username))


def _add_ppas(ppas: set[str]):
    # Add PPAs to the system
    for ppa in ppas:
        os.system(f"add-apt-repository -y {ppa}")
        LOGGER.info(f"Added PPA: {ppa}")

    # Update package list after adding PPAs
    os.system("apt update")
    LOGGER.info("Updated package list after adding PPAs")


def _install_packages(packages: set[str]):
    # Install required packages
    os.system(f"sudo apt install -y {' '.join(packages)}")
    LOGGER.info(f"Installed packages: {', '.join(packages)}")


def _install_and_update_rust(username: str):
    # Install rustup if not already installed
    # if not shutil.which("rustup"):
    #     os.system("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
    #     LOGGER.info("Installed rustup")

    # Update rustup and install the latest stable version of Rust
    _run_as_user(username, "rustup default stable")
    # install cargo packages
    _run_as_user(username, f"cargo install {' '.join(RUST_PACKAGES)}")
    # install cargo binstall packages
    _run_as_user(username, f"cargo binstall -y {' '.join(RUST_BINSTALL_PACKAGES)}")


# recursive copy of files in the ./files directory into the root filesystem
def _recursive_copy_files(src, dst):
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


def _run_as_user(username: str, command: str):
    """
    Run a shell command as a specific user.
    """
    full_command = f'su - {username} -c "{command}"'
    result = os.system(full_command)
    if result != 0:
        LOGGER.error(f"Command failed: {command}")
    else:
        LOGGER.info(f"Successfully ran command as {username}: {command}")


if __name__ == "__main__":
    main()
