import shutil

COMPILERS = {}


def register(name, exe):
    path = shutil.which(exe)
    if path:
        COMPILERS[name] = {
            "path": path,
            "exe": exe
        }


# Регистрируем поддерживаемые компиляторы
register("gcc", "gcc")
register("g++", "g++")
register("clang", "clang")
register("clang++", "clang++")
register("cl", "cl")  # MSVC