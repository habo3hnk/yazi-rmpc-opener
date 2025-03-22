#!/usr/bin/env python

import subprocess
import sys
import json
import logging
import argparse


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_rmpc_status():
    try:
        status_json = subprocess.run(
            ["rmpc", "status"], text=True, capture_output=True, check=True
        )
        status = json.loads(status_json.stdout)
        return status
    except subprocess.CalledProcessError as e:
        logging.error(f"Error getting rmpc status: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from rmpc status: {e}")
        sys.exit(1)


def select_last_added_track(playlist_len, current_track_number):
    for _ in range(playlist_len - current_track_number):
        try:
            subprocess.run(["rmpc", "next"], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error selecting next track: {e}")
            sys.exit(1)


def add_tracks_to_queue(tracks, rmpc_status):
    for track in tracks:
        try:
            subprocess.run(["rmpc", "add", track], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error adding track {track} to queue: {e}")
            sys.exit(1)

    if rmpc_status["state"] != "Stop" and len(tracks) == 1:
        playlist_len = int(rmpc_status["playlistlength"])
        current_track_number = int(rmpc_status["song"])
        select_last_added_track(playlist_len, current_track_number)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Add tracks to the rmpc queue and play them."
    )
    parser.add_argument("tracks", nargs="+", help="List of tracks to add to the queue.")
    return parser.parse_args()


def main():
    args = parse_arguments()

    rmpc_status = get_rmpc_status()

    add_tracks_to_queue(args.tracks, rmpc_status)

    try:
        subprocess.run(["rmpc", "play"], check=True)
        subprocess.run(["rmpc"], check=True)

    except subprocess.CalledProcessError as e:
        logging.error(f"Error playing tracks: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
