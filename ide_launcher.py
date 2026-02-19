import os
import subprocess


def launch_ide(ide, project_path):
    if not ide or not ide.get("path"):
        raise RuntimeError("IDE не выбрана или путь отсутствует")

    ide_path = ide["path"]

    if not os.path.isfile(ide_path):
        raise RuntimeError("Файл IDE не найден: " + ide_path)

    env = os.environ.copy()

    # Добавляем папку BuildSpy в PATH
    buildspy_path = os.path.dirname(os.path.abspath(__file__))
    env["PATH"] = buildspy_path + os.pathsep + env["PATH"]

    subprocess.Popen(
        [ide_path, project_path],
        env=env
    )