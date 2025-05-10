#!/usr/bin/env python3
# install base files and executables required for all host configurations.
import logging
import os
import shutil
from pathlib import Path

MAIN_DIR = Path(__file__).resolve().parent.parent
FILES_DIR = os.path.join(MAIN_DIR, "files")
LOGGER = logging.getLogger("install-base")
PACKAGES = {
    # helpful utility to visualize disk usage.
    "ncdu",
    # window manager I prefer to use
    "sway",
    # for IME support
    "fcitx5",
    "fcitx5-mozc",
}


def main():
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

    _install_packages(PACKAGES)
    _recursive_copy_files(FILES_DIR, "/")


def _install_packages(packages: set[str]):
    # Install required packages
    os.system(f"sudo apt -y {' '.join(packages)}")
    LOGGER.info(f"Installed packages: {', '.join(packages)}")


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


if __name__ == "__main__":
    main()
