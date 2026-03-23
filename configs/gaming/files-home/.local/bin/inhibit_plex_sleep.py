#!/usr/bin/env python3

"""
Plex Sleep Inhibitor

Checks if the 'Plex Transcoder' process is running, and if so, uses `systemd-inhibit`
to prevent the system from sleeping while streams are active.
"""

import subprocess
import time
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_plex_transcoder_running():
    try:
        # pgrep returns 0 if matches are found, 1 otherwise
        result = subprocess.run(["pgrep", "-f", "Plex Transcoder"], capture_output=True)
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Error checking for Plex Transcoder: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Inhibit system sleep when Plex Transcoder is running.")
    parser.add_argument("--interval", type=int, default=60,
                        help="Polling interval / inhibit duration in seconds")

    args = parser.parse_args()

    logging.info(f"Starting Plex Sleep Inhibitor (Process Monitor). Polling every {args.interval} seconds.")

    while True:
        if is_plex_transcoder_running():
            logging.info(f"'Plex Transcoder' process is running. Inhibiting sleep for {args.interval} seconds.")
            # systemd-inhibit holds the inhibition lock while the specified command runs.
            # Running 'sleep' effectively blocks system sleep for the sleep duration.
            start_time = time.time()
            subprocess.run([
                "systemd-inhibit",
                "--what=sleep",
                "--who=Plex_Sleep_Inhibitor",
                "--why=Plex Transcoder is running",
                "--mode=block",
                "sleep", str(args.interval)
            ])
            elapsed = time.time() - start_time
            if elapsed < args.interval:
                time.sleep(max(0, args.interval - elapsed))
        else:
            time.sleep(args.interval)

if __name__ == "__main__":
    main()
