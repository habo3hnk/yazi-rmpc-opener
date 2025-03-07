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


def add_track_to_queue(track, rmpc_status):
    subprocess.run(['rmpc', "add", track])

    if rmpc_status["state"] != "Stop":
        subprocess.run(['rmpc', "next"])


def main():
    if len(sys.argv) < 2:
        print("No argv")
        sys.exit(0)

    rmpc_status = get_rmpc_status()

    for track in sys.argv[1:]:
        add_track_to_queue(track, rmpc_status)

    subprocess.run(['rmpc', "play"])
    subprocess.run(['rmpc'])

if __name__ == "__main__":
    main()
