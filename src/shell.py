"""Ядро эмулятора: выполнение команд и стартовых скриптов.

Модуль не зависит от GUI, поэтому его удобно тестировать.
"""

from dataclasses import dataclass

from commands import COMMANDS, CommandError
from line_parser import ParseError, parse_line
from xml_logger import XmlLogger

STATUS_OK = "ok"
STATUS_ERROR = "error"


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

    def __init__(self, config):
        """Создаёт оболочку с заданными настройками."""
        self.config = config
        self.logger = XmlLogger(config.log_path)
        self.exit_requested = False
        self.exit_code = 0

    @property
    def prompt(self):
        """Строка приглашения, похожая на приглашение UNIX."""
        return f"user@{self.config.vfs_name}:~$ "

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
            self.logger.log(name, args, STATUS_ERROR, "unknown command")
            return Result(f"{name}: команда не найдена", ok=False)
        try:
            output = handler(self, args)
        except CommandError as error:
            self.logger.log(name, args, STATUS_ERROR, str(error))
            return Result(str(error), ok=False)
        self.logger.log(name, args, STATUS_OK)
        return Result(output)

    def run_script(self, path, echo):
        """Выполняет стартовый скрипт построчно.

        Каждая команда и её вывод передаются в функцию ``echo``,
        имитируя диалог с пользователем. Пустые строки и строки,
        начинающиеся с ``#``, пропускаются. При первой ошибке
        выполнение скрипта останавливается.

        Returns:
            True, если скрипт выполнен полностью без ошибок.
        """
        try:
            with open(path, encoding="utf-8") as file:
                lines = file.read().splitlines()
        except OSError as error:
            echo(f"ошибка стартового скрипта: {error}")
            return False
        for number, line in enumerate(lines, start=1):
            if not self._run_script_line(line, number, echo):
                return False
        return True

    def _run_script_line(self, line, number, echo):
        """Выполняет одну строку скрипта. Возвращает False при ошибке."""
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            return True
        echo(self.prompt + stripped)
        result = self.execute(stripped)
        if result.output:
            echo(result.output)
        if not result.ok:
            echo(f"ошибка в стартовом скрипте, строка {number}: "
                 "выполнение остановлено")
            return False
        return not self.exit_requested
