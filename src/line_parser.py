"""Парсер командной строки эмулятора.

Разбивает строку на слова с учётом одинарных и двойных кавычек,
как это делает оболочка UNIX. Символ ``#`` в начале слова
начинает комментарий до конца строки.
"""

QUOTES = ("'", '"')
COMMENT = "#"


class ParseError(Exception):
    """Ошибка разбора командной строки (например, незакрытая кавычка)."""


class Tokenizer:
    """Посимвольный разборщик строки на слова."""

    def __init__(self):
        """Создаёт пустое состояние разбора."""
        self.tokens = []
        self.current = []
        self.quote = None
        self.started = False

    def feed(self, char):
        """Обрабатывает один символ.

        Возвращает False, если начался комментарий и разбор надо
        прекратить, иначе True.
        """
        if self.quote:
            self._feed_quoted(char)
        elif char in QUOTES:
            self.quote = char
            self.started = True
        elif char.isspace():
            self.flush()
        elif char == COMMENT and not self.started:
            return False
        else:
            self.current.append(char)
            self.started = True
        return True

    def _feed_quoted(self, char):
        """Обрабатывает символ внутри кавычек."""
        if char == self.quote:
            self.quote = None
        else:
            self.current.append(char)

    def flush(self):
        """Завершает текущее слово и добавляет его в список."""
        if self.started:
            self.tokens.append("".join(self.current))
        self.current = []
        self.started = False


def parse_line(line):
    """Разбирает строку на список слов.

    Пример: ``cd "My Documents" x`` -> ``['cd', 'My Documents', 'x']``.
    Пустые кавычки ``""`` дают пустой аргумент.

    Raises:
        ParseError: если кавычка не закрыта.
    """
    tokenizer = Tokenizer()
    for char in line:
        if not tokenizer.feed(char):
            break
    if tokenizer.quote:
        raise ParseError(f"незакрытая кавычка {tokenizer.quote}")
    tokenizer.flush()
    return tokenizer.tokens
