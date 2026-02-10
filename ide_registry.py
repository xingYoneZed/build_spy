import os
import shutil
import glob

def detect_ides():
    """
    Возвращает список словарей с найденными IDE на машине.
    Каждый словарь содержит:
    {
        'name': 'VS Code',
        'path': 'C:\\Program Files\\Microsoft VS Code\\Code.exe',
        'type': 'vscode'
    }
    """
    ides = []

    # 1. Проверка стандартных IDE в PATH
    path_candidates = {
        "VS Code": "code",
        "Eclipse": "eclipse",
        "CLion": "clion",
        "Visual Studio": "devenv",
        "Keil": "uvision",
        "IAR": "iar"
    }

    for name, exe_name in path_candidates.items():
        path = shutil.which(exe_name)
        if path:
            ides.append({"name": name, "path": path, "type": name.lower().replace(" ", "_")})

    # 2. Поиск в стандартных директориях
    search_dirs = [
        os.environ.get("ProgramFiles", "C:\\Program Files"),
        os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
        "C:\\Tools",
        "C:\\Keil",
        "C:\\IAR",
        "C:\\ST",
        "C:\\STM32"
    ]

    search_patterns = {
        "VS Code": ["Code.exe"],
        "Eclipse": ["eclipse*.exe", "stm32*.exe"],
        "CLion": ["clion*.exe"],
        "Keil": ["uvision*.exe"],
        "IAR": ["iar*.exe"],
        "Visual Studio": ["devenv.exe"]
    }

    for base_dir in search_dirs:
        if not os.path.isdir(base_dir):
            continue
        for ide_name, patterns in search_patterns.items():
            for pattern in patterns:
                for exe_path in glob.glob(os.path.join(base_dir, "**", pattern), recursive=True):
                    exe_path = os.path.abspath(exe_path)
                    if os.path.isfile(exe_path) and not any(d['path'] == exe_path for d in ides):
                        ides.append({"name": ide_name, "path": exe_path, "type": ide_name.lower().replace(" ", "_")})

    return ides