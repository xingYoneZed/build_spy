import json
import os

BUILD_LOG = "build.jsonl"
REPORT_FILE = "report.json"


def analyze(project_root):
    used_sources = set()
    used_headers = set()

    if not os.path.exists(BUILD_LOG):
        return

    with open(BUILD_LOG, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            parsed = entry.get("parsed", {})
            used_sources.update(parsed.get("sources", []))
            used_headers.update(parsed.get("headers", []))

    all_files = []
    for root, _, files in os.walk(project_root):
        for f in files:
            all_files.append(os.path.join(root, f))

    unused = [
        f for f in all_files
        if f.endswith((".c", ".cpp", ".h"))
        and f not in used_sources
        and f not in used_headers
    ]

    grouped = {}
    for f in unused:
        folder = os.path.dirname(f)
        grouped.setdefault(folder, []).append(os.path.basename(f))

    report = {
        "project_root": project_root,
        "unused_grouped": grouped
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report