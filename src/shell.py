"""Ядро эмулятора: разбор и выполнение команд.

Модуль не зависит от GUI, поэтому его удобно тестировать.
"""

from dataclasses import dataclass

from commands import COMMANDS, CommandError
from line_parser import ParseError, parse_line

DEFAULT_VFS_NAME = "vfs"


@dataclass
class Result:
    """Результат выполнения одной строки.

    Attributes:
        output: текст для вывода на экран.
        ok: True, если команда выполнена без ошибок.
    """

    output: str
    ok: bool = True


class Shell:
    """Командная оболочка эмулятора."""

    def __init__(self, vfs_name=DEFAULT_VFS_NAME):
        """Создаёт оболочку для VFS с заданным именем."""
        self.vfs_name = vfs_name
        self.exit_requested = False
        self.exit_code = 0

    @property
    def prompt(self):
        """Строка приглашения, похожая на приглашение UNIX."""
        return f"user@{self.vfs_name}:~$ "

    def request_exit(self, code):
        """Помечает, что пользователь запросил выход."""
        self.exit_requested = True
        self.exit_code = code

    def execute(self, line):
        """Разбирает и выполняет одну строку ввода."""
        try:
            words = parse_line(line)
        except ParseError as error:
            return Result(f"ошибка разбора: {error}", ok=False)
        if not words:
            return Result("")
        name, args = words[0], words[1:]
        handler = COMMANDS.get(name)
        if handler is None:
            return Result(f"{name}: команда не найдена", ok=False)
        try:
            return Result(handler(self, args))
        except CommandError as error:
            return Result(str(error), ok=False)
