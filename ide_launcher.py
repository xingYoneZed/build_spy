import os
import subprocess
from ide_registry import detect_ides

def launch_ide(ide, project_root):
    """
    Запускает выбранную IDE с указанным проектом.
    ide: словарь из detect_ides()
    project_root: путь к проекту
    """
    if ide is None or not ide.get("path"):
        raise RuntimeError("Выбранная IDE не найдена или путь пустой")

    exe_path = ide["path"]

    # Защита: BuildSpy не запускаем внутри себя
    if os.path.basename(exe_path).lower().startswith("buildspy"):
        raise RuntimeError("Нельзя открыть BuildSpy внутри BuildSpy")

    # Команда для запуска IDE с проектом
    cmd = []

    ide_type = ide["type"]

    if ide_type in ["vscode"]:
        cmd = [exe_path, project_root]
    elif ide_type in ["eclipse", "stm32cubeide"]:
        # Eclipse-подобные IDE открываются через workspace
        cmd = [exe_path, "-data", project_root]
    elif ide_type in ["keil", "iar", "clion"]:
        # Проектные IDE
        cmd = [exe_path, project_root]
    elif ide_type in ["visual_studio"]:
        cmd = [exe_path, project_root]
    else:
        # fallback
        cmd = [exe_path, project_root]

    # Запуск процесса
    try:
        subprocess.Popen(cmd)
    except Exception as e:
        raise RuntimeError(f"Не удалось запустить IDE {ide['name']}: {e}")

def get_ides_list():
    """
    Возвращает список доступных IDE для GUI.
    """
    return detect_ides()