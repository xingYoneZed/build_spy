import sys
import subprocess
from spy_core import log_entry
from compiler_config import COMPILERS


def main():
    if len(sys.argv) < 2:
        print("[BuildSpy] No compiler name provided")
        sys.exit(1)

    compiler_key = sys.argv[1]
    real_args = sys.argv[2:]

    if compiler_key not in COMPILERS:
        print(f"[BuildSpy] Unknown compiler wrapper: {compiler_key}")
        sys.exit(1)

    compiler = COMPILERS[compiler_key]

    log_entry(
        compiler=compiler_key,
        argv=real_args
    )

    cmd = [compiler["path"]] + real_args
    result = subprocess.run(cmd)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()