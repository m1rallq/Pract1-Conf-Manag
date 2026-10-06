"""Графический интерфейс эмулятора на tkinter."""

import tkinter as tk
from tkinter import scrolledtext

FONT = ("Consolas", 11)
BG_COLOR = "#1e1e1e"
FG_COLOR = "#d4d4d4"
ERROR_COLOR = "#f48771"
WINDOW_SIZE = "800x500"


class ShellWindow:
    """Окно терминала: область вывода и строка ввода."""

    def __init__(self, shell):
        """Создаёт окно для заданной оболочки."""
        self.shell = shell
        self.root = tk.Tk()
        self.root.title(f"Эмулятор оболочки — VFS: {shell.config.vfs_name}")
        self.root.geometry(WINDOW_SIZE)
        self._build_output()
        self._build_input()

    def _build_output(self):
        """Создаёт область вывода только для чтения."""
        self.output = scrolledtext.ScrolledText(
            self.root, font=FONT, bg=BG_COLOR, fg=FG_COLOR,
            state=tk.DISABLED, wrap=tk.WORD,
        )
        self.output.tag_config("error", foreground=ERROR_COLOR)
        self.output.pack(fill=tk.BOTH, expand=True)

    def _build_input(self):
        """Создаёт строку приглашения и поле ввода."""
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(fill=tk.X)
        tk.Label(frame, text=self.shell.prompt, font=FONT,
                 bg=BG_COLOR, fg=FG_COLOR).pack(side=tk.LEFT)
        self.entry = tk.Entry(frame, font=FONT, bg=BG_COLOR, fg=FG_COLOR,
                              insertbackground=FG_COLOR)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()

    def print(self, text, error=False):
        """Добавляет строку в область вывода."""
        self.output.configure(state=tk.NORMAL)
        tags = ("error",) if error else ()
        self.output.insert(tk.END, text + "\n", tags)
        self.output.configure(state=tk.DISABLED)
        self.output.see(tk.END)

    def _on_enter(self, _event):
        """Выполняет введённую команду по нажатию Enter."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.print(self.shell.prompt + line)
        result = self.shell.execute(line)
        if result.output:
            self.print(result.output, error=not result.ok)
        self._close_if_exit()

    def _close_if_exit(self):
        """Закрывает окно, если была вызвана команда exit."""
        if self.shell.exit_requested:
            self.root.after(0, self.root.destroy)

    def run(self, startup_lines=(), script_path=None):
        """Показывает стартовые строки, выполняет скрипт и запускает окно."""
        for line in startup_lines:
            self.print(line)
        if script_path:
            self.root.after(0, self._run_script, script_path)
        self.root.mainloop()

    def _run_script(self, script_path):
        """Выполняет стартовый скрипт с выводом в окно."""
        self.print(f"--- выполнение скрипта {script_path} ---")
        self.shell.run_script(script_path, self.print)
        self._close_if_exit()
