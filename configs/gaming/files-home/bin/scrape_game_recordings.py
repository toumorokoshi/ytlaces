#!/usr/bin/env python3
import os
import glob
import subprocess
from pathlib import Path
from typing import List

def convert_steam_recordings() -> None:
    """
    Finds and converts Steam game recordings to MP4 format using pathlib.

    This script uses Path objects for a more modern and object-oriented
    approach to file system operations. It looks for directories prefixed
    with 'bg_330020' in the specified Steam recording path and converts
    the 'session.mpd' file in each into an MP4 video using ffmpeg.
    
    The script now extracts the date directly from the directory name
    to name the output file.
    """
    # --- Configuration ---
    # Get the user's home directory as a Path object
    home_dir: Path = Path.home()
    
    # Define the base directory for game recordings using the '/' operator
    base_dir: Path = home_dir / '.local' / 'share' / 'Steam' / 'userdata' / \
               '3869537' / 'gamerecordings' / 'video'

    # Define the output directory for the converted MP4 files
    output_dir: Path = home_dir / 'Videos'

    # Ensure the output directory exists, creating it if necessary
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- Find the recording directories ---
    # Use glob() on the Path object to find all directories matching the prefix
    recording_dirs: List[Path] = list(base_dir.glob('bg_330020*'))

    if not recording_dirs:
        print(f"No directories found with prefix 'bg_330020' in {base_dir}")
        return

    print(f"Found {len(recording_dirs)} recording directories to process.")

    # --- Process each recording directory ---
    for recording_path in recording_dirs:
        # Extract the date from the directory name
        # The directory name format is assumed to be 'bg_330020_YYYY_MM_DD_...'
        try:
            _, date_str = recording_path.name.split('_', 1)
        except IndexError:
            print(f"Skipping directory due to unexpected name format: {recording_path.name}")
            continue

        # Construct the input file path using the '/' operator
        input_file: Path = recording_path / 'session.mpd'
        
        # Create the output filename using the extracted date
        output_filename: str = f"{date_str}.mp4"
        output_file_path: Path = output_dir / output_filename

        if output_file_path.exists():
            print(f"{output_file_path} exists. skipping...")
            continue

        print(f"Processing '{input_file}' -> '{output_file_path}'")

        # Construct the ffmpeg command as a list of strings
        command: List[str] = [
            'ffmpeg',
            '-i', str(input_file),
            '-c', 'copy',
            str(output_file_path)
        ]
        
        try:
            # Use subprocess.run to execute the command
            subprocess.run(command, capture_output=True, text=True, check=True)
            print(f"Successfully converted and saved to '{output_file_path}'")
        except FileNotFoundError:
            print("Error: `ffmpeg` command not found. Please make sure ffmpeg is installed and in your system's PATH.")
            break
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running ffmpeg:")
            print(f"  Return code: {e.returncode}")
            print(f"  Stdout: {e.stdout}")
            print(f"  Stderr: {e.stderr}")
            continue
        
    print("\nConversion process finished.")

if __name__ == "__main__":
    convert_steam_recordings()

