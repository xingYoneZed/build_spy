import os
from pathlib import Path

def create_spy_env(spy_dir: Path, real_gcc: Path, log_file: Path):
    env = os.environ.copy()

    env["REAL_GCC_PATH"] = str(real_gcc)
    env["GCC_SPY_LOG"] = str(log_file)

    # Подменяем PATH
    env["PATH"] = str(spy_dir) + os.pathsep + env["PATH"]

    return env