"""Встроенные команды эмулятора.

Каждая команда — функция ``(shell, args) -> str``, которая
возвращает текст вывода или выбрасывает CommandError.
"""

LS_OPTIONS = ("-l", "-a", "-la", "-al")
CD_MAX_ARGS = 1
EXIT_MAX_ARGS = 1


class CommandError(Exception):
    """Ошибка выполнения команды (неверные аргументы и т.п.)."""


def _stub_output(name, args):
    """Формирует вывод команды-заглушки: имя и аргументы."""
    if not args:
        return f"{name}: вызвана без аргументов"
    quoted = ", ".join(f"'{arg}'" for arg in args)
    return f"{name}: аргументы [{quoted}]"


def cmd_ls(shell, args):
    """Заглушка ls: проверяет опции и выводит имя и аргументы."""
    for arg in args:
        if arg.startswith("-") and arg not in LS_OPTIONS:
            raise CommandError(f"ls: неверный ключ '{arg}'")
    return _stub_output("ls", args)


def cmd_cd(shell, args):
    """Заглушка cd: принимает не более одного аргумента."""
    if len(args) > CD_MAX_ARGS:
        raise CommandError("cd: слишком много аргументов")
    return _stub_output("cd", args)


def cmd_exit(shell, args):
    """Завершает работу эмулятора с необязательным кодом выхода."""
    if len(args) > EXIT_MAX_ARGS:
        raise CommandError("exit: слишком много аргументов")
    code = 0
    if args:
        try:
            code = int(args[0])
        except ValueError as error:
            raise CommandError(
                f"exit: требуется числовой аргумент: {args[0]}"
            ) from error
    shell.request_exit(code)
    return "exit"


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}
