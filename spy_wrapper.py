import sys
import subprocess
import os
import json
from datetime import datetime
from compiler_config import COMPILERS


LOG_FILE = "build.jsonl"


def log_entry(entry):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    if len(sys.argv) < 2:
        print("[BuildSpy] No compiler name provided")
        sys.exit(1)

    compiler_name = sys.argv[1]
    real_args = sys.argv[2:]

    if compiler_name not in COMPILERS:
        print(f"[BuildSpy] Unknown compiler: {compiler_name}")
        sys.exit(1)

    compiler_path = COMPILERS[compiler_name]["path"]

    if not compiler_path or not os.path.isfile(compiler_path):
        print(f"[BuildSpy] Real compiler not found: {compiler_path}")
        sys.exit(1)

    # логируем вызов
    log_entry({
        "timestamp": datetime.now().isoformat(),
        "compiler": compiler_name,
        "args": real_args,
        "cwd": os.getcwd()
    })

    # запускаем настоящий компилятор
    cmd = [compiler_path] + real_args
    result = subprocess.run(cmd)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()