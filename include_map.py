import subprocess
import os


def collect_includes(source, project_root):
    cmd = ["gcc", "-M", source]

    try:
        result = subprocess.check_output(
            cmd,
            stderr=subprocess.DEVNULL,
            text=True
        )
    except subprocess.CalledProcessError:
        return set()

    parts = result.replace("\\\n", "").split(":")
    if len(parts) < 2:
        return set()

    deps = parts[1].strip().split()
    includes = set()

    for dep in deps:
        dep = os.path.abspath(dep)
        if dep.startswith(project_root) and dep.endswith(".h"):
            includes.add(dep)

    return includes