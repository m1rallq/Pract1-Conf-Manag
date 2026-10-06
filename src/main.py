"""Точка входа эмулятора командной оболочки.

Пример запуска::

    python src/main.py
"""

import sys

from gui import ShellWindow
from shell import Shell


def main():
    """Создаёт оболочку и открывает окно эмулятора."""
    shell = Shell()
    ShellWindow(shell).run()
    return shell.exit_code


if __name__ == "__main__":
    sys.exit(main())
