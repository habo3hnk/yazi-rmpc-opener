#!/usr/bin/env python

import subprocess
import sh
import sys
import json
import logging
import argparse
from enum import Enum


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class RmpcCommand(Enum):
    STATUS = "status"
    ADD = "add"
    NEXT = "next"
    PLAY = "play"


class RmpcClient:
    def __init__(self):
        self.status = None

    def get_status(self):
        if not self.status:
            output = sh.rmpc(RmpcCommand.STATUS.value)
            try:
                self.status = json.loads(output)
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON from rmpc status: {e}")
                raise
        return self.status

    def select_last_added_track(self, playlist_len, current_track_number):
        for _ in range(playlist_len - current_track_number):
            try:
                sh.rmpc(RmpcCommand.NEXT.value)
            except Exception as e:
                logging.error(f"Error selecting next track: {e}")
                sys.exit(1)

    def add_tracks_to_queue(self, tracks):
        rmpc_status = self.get_status()

        for track in tracks:
            try:
                sh.rmpc(RmpcCommand.ADD.value, track)
            except Exception as e:
                logging.error(f"Error adding track {track} to queue: {e}")
                sys.exit(1)

        if rmpc_status["state"] != "Stop" and len(tracks) == 1:
            playlist_len = int(rmpc_status["playlistlength"])
            current_track_number = int(rmpc_status["song"])
            self.select_last_added_track(playlist_len, current_track_number)

    def play(self):
        sh.rmpc(RmpcCommand.PLAY.value)
        subprocess.run(["rmpc"], check=True)


class RmpcApp:
    def __init__(self):
        self.client = RmpcClient()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description="Add tracks to the rmpc queue and play them."
        )
        parser.add_argument(
            "tracks", nargs="+", help="List of tracks to add to the queue."
        )
        return parser.parse_args()

    def main(self):
        args = self.parse_arguments()

        try:
            self.client.add_tracks_to_queue(args.tracks)
            self.client.play()
        except Exception as e:
            logging.error(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    app = RmpcApp()
    app.main()
