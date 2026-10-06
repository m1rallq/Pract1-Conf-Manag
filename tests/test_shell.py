"""Тесты команд и оболочки."""

import unittest

from shell import Shell


class CommandsTest(unittest.TestCase):
    """Проверка встроенных команд."""

    def setUp(self):
        """Создаёт оболочку."""
        self.shell = Shell("myvfs")

    def test_prompt_has_vfs_name(self):
        """Приглашение содержит имя VFS."""
        self.assertIn("myvfs", self.shell.prompt)

    def test_ls_prints_args(self):
        """ls выводит своё имя и аргументы."""
        result = self.shell.execute('ls -l "my dir"')
        self.assertTrue(result.ok)
        self.assertIn("ls", result.output)
        self.assertIn("'my dir'", result.output)

    def test_ls_bad_option(self):
        """Неизвестный ключ ls — ошибка."""
        self.assertFalse(self.shell.execute("ls -z").ok)

    def test_cd_prints_args(self):
        """cd выводит своё имя и аргумент."""
        result = self.shell.execute("cd docs")
        self.assertTrue(result.ok)
        self.assertIn("'docs'", result.output)

    def test_cd_too_many_args(self):
        """cd с двумя аргументами — ошибка."""
        self.assertFalse(self.shell.execute("cd a b").ok)

    def test_unknown_command(self):
        """Неизвестная команда — ошибка."""
        result = self.shell.execute("foo")
        self.assertFalse(result.ok)
        self.assertIn("команда не найдена", result.output)

    def test_parse_error(self):
        """Незакрытая кавычка — ошибка разбора."""
        self.assertFalse(self.shell.execute('cd "abc').ok)

    def test_exit(self):
        """exit выставляет флаг выхода и код."""
        self.shell.execute("exit 3")
        self.assertTrue(self.shell.exit_requested)
        self.assertEqual(self.shell.exit_code, 3)

    def test_exit_bad_arg(self):
        """exit с нечисловым аргументом — ошибка."""
        self.assertFalse(self.shell.execute("exit abc").ok)
        self.assertFalse(self.shell.exit_requested)


if __name__ == "__main__":
    unittest.main()
