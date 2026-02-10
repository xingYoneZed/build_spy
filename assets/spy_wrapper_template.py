import os
import json
import subprocess
from collections import deque

LOG_FILE = "build.jsonl"
REPORT_FILE = "report.json"


def load_build_log():
    entries = []
    if not os.path.exists(LOG_FILE):
        return entries

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return entries


def scan_project(project_root):
    sources, headers = set(), set()
    for root, _, files in os.walk(project_root):
        for f in files:
            path = os.path.abspath(os.path.join(root, f))
            if f.endswith(".c"):
                sources.add(path)
            elif f.endswith(".h"):
                headers.add(path)
    return sources, headers


def collect_includes(file_path, project_root):
    try:
        out = subprocess.check_output(
            ["gcc", "-M", file_path],
            stderr=subprocess.DEVNULL,
            text=True
        )
    except subprocess.CalledProcessError:
        return set()

    out = out.replace("\\\n", "")
    parts = out.split(":")
    if len(parts) < 2:
        return set()

    headers = set()
    for dep in parts[1].split():
        dep = os.path.abspath(dep)
        if dep.startswith(project_root) and dep.endswith(".h"):
            headers.add(dep)
    return headers


def build_include_graph(files, project_root):
    return {f: collect_includes(f, project_root) for f in files}


def traverse(start_files, graph):
    visited = set()
    q = deque(start_files)

    while q:
        cur = q.popleft()
        if cur in visited:
            continue
        visited.add(cur)
        for dep in graph.get(cur, []):
            if dep not in visited:
                q.append(dep)

    return visited


def is_maybe_header(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
            return any(k in data for k in ("#ifdef", "#ifndef", "#if", "#define"))
    except OSError:
        return False


def analyze(project_root):
    entries = load_build_log()

    used_sources = set()
    for e in entries:
        for s in e.get("sources", []):
            s = os.path.abspath(s)
            if s.startswith(project_root):
                used_sources.add(s)

    all_sources, all_headers = scan_project(project_root)
    graph = build_include_graph(all_sources | all_headers, project_root)

    reachable = traverse(used_sources, graph)

    used_headers = {f for f in reachable if f.endswith(".h")}
    used_sources = {f for f in reachable if f.endswith(".c")}

    unused_sources = sorted(all_sources - used_sources)

    unused_headers = []
    maybe_headers = []

    for h in all_headers:
        if h in used_headers:
            continue
        if is_maybe_header(h):
            maybe_headers.append(h)
        else:
            unused_headers.append(h)

    report = {
        "project_root": project_root,
        "used": {
            "sources": sorted(used_sources),
            "headers": sorted(used_headers),
        },
        "unused": {
            "sources": unused_sources,
            "headers": sorted(unused_headers),
        },
        "maybe": {
            "headers": sorted(maybe_headers)
        }
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n[USED]")
    print(" sources:", len(used_sources))
    print(" headers:", len(used_headers))

    print("\n[UNUSED]")
    for f in unused_sources or ["(нет)"]:
        print(" ", f)
    for f in unused_headers or ["(нет)"]:
        print(" ", f)

    print("\n[MAYBE]")
    for f in maybe_headers or ["(нет)"]:
        print(" ", f)

    print(f"\n[OK] Отчёт сохранён в {REPORT_FILE}")


def main():
    analyze(os.path.abspath(os.getcwd()))


if __name__ == "__main__":
    main()