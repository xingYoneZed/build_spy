import json
import os
import datetime

LOG_FILE = os.environ.get("GCC_SPY_LOG", "build.jsonl")


def log_entry(compiler: str, argv: list):
    entry = {
        "time": datetime.datetime.now().isoformat(),
        "cwd": os.getcwd(),
        "compiler": compiler,
        "argv": argv,
        "parsed": parse_args(argv)
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def parse_args(argv):
    sources = []
    include_dirs = []
    output = None
    other_args = []

    it = iter(argv)
    for arg in it:
        if arg.endswith((".c", ".cpp", ".cc", ".cxx")):
            sources.append(arg)
        elif arg.startswith("-I"):
            if arg == "-I":
                include_dirs.append(next(it, ""))
            else:
                include_dirs.append(arg[2:])
        elif arg == "-o":
            output = next(it, None)
        else:
            other_args.append(arg)

    return {
        "sources": sources,
        "include_dirs": include_dirs,
        "output": output,
        "other_args": other_args
    }