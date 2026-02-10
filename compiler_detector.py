import shutil
import subprocess
from pathlib import Path


def find_in_path(names):
    found = {}
    for name in names:
        path = shutil.which(name)
        if path:
            found[name] = path
    return found


def find_gcc():
    return find_in_path(["gcc", "g++"])


def find_clang():
    return find_in_path(["clang", "clang++"])


def find_msvc():
    vswhere = Path(
        r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
    )
    if not vswhere.exists():
        return None

    result = subprocess.run(
        [
            str(vswhere),
            "-latest",
            "-products",
            "*",
            "-requires",
            "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
            "-property",
            "installationPath",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0 or not result.stdout.strip():
        return None

    vs_path = Path(result.stdout.strip())
    cl = list(vs_path.rglob("cl.exe"))
    return str(cl[0]) if cl else None


def detect_compilers():
    compilers = {}

    gcc = find_gcc()
    if gcc:
        compilers["GCC"] = gcc["gcc"]

    clang = find_clang()
    if clang:
        compilers["Clang"] = clang["clang"]

    msvc = find_msvc()
    if msvc:
        compilers["MSVC"] = msvc

    return compilers


if __name__ == "__main__":
    for name, path in detect_compilers().items():
        print(f"{name}: {path}")