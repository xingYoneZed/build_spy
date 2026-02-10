import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import time
import threading
import json

from ide_launcher import launch_ide
from ide_registry import detect_ides
from analyzer_build import analyze

BUILD_LOG = "build.jsonl"
REPORT_FILE = "report.json"


class BuildSpyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BuildSpy")
        self.geometry("900x500")

        self.project_root = tk.StringVar(value="")
        self.selected_ide = tk.StringVar()

        self.ide_map = {}
        self.last_build_mtime = None

        self._build_ui()
        self._start_build_watcher()

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        # ---- Проект ----
        ttk.Label(top, text="Проект:").pack(side="left")

        ttk.Entry(
            top,
            textvariable=self.project_root,
            width=50,
            state="readonly"
        ).pack(side="left", padx=5)

        ttk.Button(
            top,
            text="Выбрать проект",
            command=self._select_project
        ).pack(side="left", padx=5)

        # ---- IDE ----
        ttk.Label(top, text="IDE:").pack(side="left", padx=10)

        ides = detect_ides()
        ide_names = []

        for ide in ides:
            if isinstance(ide, dict):
                name = ide.get("name", "Unknown IDE")
                self.ide_map[name] = ide
                ide_names.append(name)
            else:
                self.ide_map[ide] = {
                    "name": ide,
                    "path": None,
                    "type": "generic"
                }
                ide_names.append(ide)

        combo = ttk.Combobox(
            top,
            values=ide_names,
            textvariable=self.selected_ide,
            state="readonly",
            width=25
        )
        combo.pack(side="left")

        if ide_names:
            combo.current(0)

        ttk.Button(
            top,
            text="Открыть IDE",
            command=self._open_ide
        ).pack(side="left", padx=10)

        # ---- Отчёт ----
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.heading("#0", text="Избыточные файлы (автоматически после сборки)")

    def _select_project(self):
        folder = filedialog.askdirectory(title="Выберите папку проекта")
        if not folder:
            return

        self.project_root.set(folder)
        self.last_build_mtime = None  # сброс отслеживания
        self.tree.delete(*self.tree.get_children())

    def _open_ide(self):
        if not self.project_root.get():
            messagebox.showwarning(
                "Проект не выбран",
                "Сначала выберите проект"
            )
            return

        name = self.selected_ide.get()
        ide = self.ide_map.get(name)

        if not ide:
            messagebox.showerror("Ошибка", "IDE не найдена")
            return

        launch_ide(ide, self.project_root.get())

    def _start_build_watcher(self):
        thread = threading.Thread(
            target=self._watch_build_log,
            daemon=True
        )
        thread.start()

    def _watch_build_log(self):
        while True:
            if self.project_root.get() and os.path.exists(BUILD_LOG):
                mtime = os.path.getmtime(BUILD_LOG)
                if self.last_build_mtime is None:
                    self.last_build_mtime = mtime
                elif mtime != self.last_build_mtime:
                    self.last_build_mtime = mtime
                    self._on_build_finished()
            time.sleep(1)

    def _on_build_finished(self):
        try:
            analyze(self.project_root.get())
            self.after(0, self._load_report)
        except Exception as e:
            self.after(
                0,
                lambda: messagebox.showerror("Ошибка анализа", str(e))
            )

    def _load_report(self):
        self.tree.delete(*self.tree.get_children())

        if not os.path.exists(REPORT_FILE):
            return

        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            report = json.load(f)

        grouped = report.get("unused_grouped", {})

        for folder, files in grouped.items():
            parent = self.tree.insert("", "end", text=folder)
            for file in files:
                self.tree.insert(parent, "end", text=file)