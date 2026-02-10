from pathlib import Path
import json
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent
ANALYZER = BASE_DIR / "analyzer_build.py"
REPORT = BASE_DIR / "report.json"


def run_analysis():
    subprocess.run(
        ["python", str(ANALYZER)],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True
    )


def load_report():
    if not REPORT.exists():
        return [], []

    with open(REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("unused_sources", []), data.get("unused_headers", [])