#!/usr/bin/env python

import subprocess
import sys
import json


def get_rmpc_status():
    status_json = subprocess.run(
        ['rmpc', "status"],
        text=True,
        capture_output=True
    )
    status = json.loads(status_json.stdout)
    return status


def select_last_added_track(playlist_len, current_track_number):
    for i in range(playlist_len - current_track_number):
        subprocess.run(['rmpc', "next"])


def add_tracks_to_queue(tracks, rmpc_status):
    for i in tracks:
        subprocess.run(['rmpc', "add", i])

    if rmpc_status["state"] != "Stop" and len(tracks)==1:
        playlist_len = int(rmpc_status["playlistlength"])
        current_track_number = int(rmpc_status["song"])
        select_last_added_track(playlist_len, current_track_number)


def main():
    if len(sys.argv) < 2:
        print("No argv")
        sys.exit(0)

    rmpc_status = get_rmpc_status()

    add_tracks_to_queue(sys.argv[1:], rmpc_status)

    subprocess.run(['rmpc', "play"])
    subprocess.run(['rmpc'])


if __name__ == "__main__":
    main()
