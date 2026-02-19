import os
import sys
import subprocess
from datetime import datetime
import json

LOG_FILE = "build.jsonl"


def log_command(command):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def find_real_make():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    for path in os.environ["PATH"].split(os.pathsep):
        real_make = os.path.join(path, "make.exe")

        if os.path.isfile(real_make) and current_dir not in real_make:
            return real_make

    return None


def main():
    real_make = find_real_make()

    if not real_make:
        print("[BuildSpy] make.exe не найден")
        sys.exit(1)

    args = sys.argv[1:]
    command = [real_make] + args

    log_command(command)

    result = subprocess.run(command)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()