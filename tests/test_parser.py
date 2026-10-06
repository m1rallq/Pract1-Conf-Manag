"""Тесты парсера командной строки."""

import unittest

from line_parser import ParseError, parse_line


class ParseLineTest(unittest.TestCase):
    """Проверка разбора строки на слова."""

    def test_simple_words(self):
        """Слова разделяются пробелами."""
        self.assertEqual(parse_line("ls -l /home"), ["ls", "-l", "/home"])

    def test_extra_spaces(self):
        """Лишние пробелы игнорируются."""
        self.assertEqual(parse_line("  cd   dir  "), ["cd", "dir"])

    def test_double_quotes(self):
        """Аргумент в двойных кавычках остаётся одним словом."""
        self.assertEqual(parse_line('cd "My Documents"'),
                         ["cd", "My Documents"])

    def test_single_quotes(self):
        """Аргумент в одинарных кавычках остаётся одним словом."""
        self.assertEqual(parse_line("ls 'a b' c"), ["ls", "a b", "c"])

    def test_nested_other_quote(self):
        """Другая кавычка внутри кавычек — обычный символ."""
        self.assertEqual(parse_line("ls \"it's\""), ["ls", "it's"])

    def test_quotes_inside_word(self):
        """Кавычки внутри слова склеиваются с ним."""
        self.assertEqual(parse_line('ls a"b c"d'), ["ls", "ab cd"])

    def test_empty_quotes(self):
        """Пустые кавычки дают пустой аргумент."""
        self.assertEqual(parse_line('cd ""'), ["cd", ""])

    def test_unclosed_quote(self):
        """Незакрытая кавычка — ошибка."""
        with self.assertRaises(ParseError):
            parse_line('cd "abc')

    def test_comment(self):
        """Всё после # в начале слова — комментарий."""
        self.assertEqual(parse_line("ls a # comment"), ["ls", "a"])

    def test_hash_inside_word(self):
        """# внутри слова не начинает комментарий."""
        self.assertEqual(parse_line("ls a#b"), ["ls", "a#b"])

    def test_empty_line(self):
        """Пустая строка даёт пустой список."""
        self.assertEqual(parse_line("   "), [])


if __name__ == "__main__":
    unittest.main()
