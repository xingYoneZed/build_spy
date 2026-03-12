import os
import subprocess


def launch_ide(ide, project_path):

    ide_path = ide["path"]

    env = os.environ.copy()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    wrappers_dir = os.path.join(base_dir, "wrappers")

    env["PATH"] = wrappers_dir + os.pathsep + env["PATH"]

    subprocess.Popen(
        [ide_path, project_path],
        env=env
    )