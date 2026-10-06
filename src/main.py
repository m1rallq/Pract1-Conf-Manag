"""Точка входа эмулятора командной оболочки.

Пример запуска::

    python src/main.py --vfs ./myvfs --log log.xml --script start.txt
"""

import sys

from config import parse_args
from gui import ShellWindow
from shell import Shell


def debug_lines(config):
    """Строки отладочного вывода параметров при запуске."""
    lines = ["[debug] параметры запуска:"]
    lines += [f"[debug]   {key} = {value or '-'}"
              for key, value in config.as_pairs()]
    return lines


def main(argv=None):
    """Разбирает параметры, печатает их и открывает окно эмулятора."""
    config = parse_args(argv)
    lines = debug_lines(config)
    print("\n".join(lines))
    shell = Shell(config)
    window = ShellWindow(shell)
    window.run(startup_lines=lines, script_path=config.script_path)
    return shell.exit_code


if __name__ == "__main__":
    sys.exit(main())
