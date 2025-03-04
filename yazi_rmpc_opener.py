#!/usr/bin/env python

import subprocess
import sys
import json

def run_rmpc_command(audio_name):
    try:
        status_json = subprocess.run(
            ['rmpc', "status"],
            text=True,
            capture_output=True
        )
        status = json.loads(status_json.stdout)
        subprocess.run(['rmpc', "add", audio_name])
        subprocess.run(['rmpc', "play"])
 
        if status["state"] != "Stop":
            subprocess.run(['rmpc', "next"])
        subprocess.run(['rmpc'])

    except FileNotFoundError:
        print("Error: rmpc is not installed.")


def main():
    if len(sys.argv) == 2:
        run_rmpc_command(sys.argv[1])
    else:
        print("No argv")

if __name__ == "__main__":
    main()
