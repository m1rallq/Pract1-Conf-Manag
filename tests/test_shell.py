"""Тесты команд, оболочки, стартовых скриптов и XML-лога."""

import os
import tempfile
import unittest
import xml.etree.ElementTree as ET

from config import Config, parse_args
from shell import Shell


class CommandsTest(unittest.TestCase):
    """Проверка встроенных команд."""

    def setUp(self):
        """Создаёт оболочку без лога."""
        self.shell = Shell(Config(vfs_path="/tmp/myvfs"))

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

    def test_conf_dump(self):
        """conf-dump выводит параметры в формате ключ=значение."""
        result = self.shell.execute("conf-dump")
        self.assertIn("vfs=/tmp/myvfs", result.output)
        self.assertIn("vfs_name=myvfs", result.output)


class ConfigTest(unittest.TestCase):
    """Проверка разбора параметров командной строки."""

    def test_all_params(self):
        """Все три параметра попадают в Config."""
        config = parse_args(["--vfs", "v", "--log", "l.xml",
                             "--script", "s.txt"])
        self.assertEqual(config.vfs_path, "v")
        self.assertEqual(config.log_path, "l.xml")
        self.assertEqual(config.script_path, "s.txt")

    def test_defaults(self):
        """Без параметров используется имя VFS по умолчанию."""
        self.assertEqual(parse_args([]).vfs_name, "vfs")


class ScriptAndLogTest(unittest.TestCase):
    """Проверка стартовых скриптов и XML-лога."""

    def setUp(self):
        """Создаёт временную папку."""
        self.tmp = tempfile.TemporaryDirectory()
        self.log_path = os.path.join(self.tmp.name, "log.xml")
        self.shell = Shell(Config(log_path=self.log_path))
        self.lines = []

    def tearDown(self):
        """Удаляет временную папку."""
        self.tmp.cleanup()

    def _script(self, text):
        """Записывает текст скрипта во временный файл."""
        path = os.path.join(self.tmp.name, "start.txt")
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        return path

    def test_script_ok(self):
        """Скрипт с комментариями выполняется полностью."""
        path = self._script("# comment\n\nls\ncd dir\n")
        self.assertTrue(self.shell.run_script(path, self.lines.append))
        self.assertTrue(any("ls" in line for line in self.lines))
        self.assertFalse(any("comment" in line for line in self.lines))

    def test_script_error_stops(self):
        """Ошибка в скрипте останавливает выполнение."""
        path = self._script("ls\nfoo\ncd dir\n")
        self.assertFalse(self.shell.run_script(path, self.lines.append))
        self.assertIn("строка 2", self.lines[-1])
        self.assertFalse(any("cd dir" in line for line in self.lines))

    def test_script_missing(self):
        """Отсутствующий скрипт — сообщение об ошибке."""
        missing = os.path.join(self.tmp.name, "nope.txt")
        self.assertFalse(self.shell.run_script(missing, self.lines.append))

    def test_xml_log(self):
        """Каждый вызов команды пишется в XML с датой и временем."""
        self.shell.execute('cd "a b"')
        self.shell.execute("foo")
        events = ET.parse(self.log_path).getroot().findall("event")
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].findtext("command"), "cd")
        self.assertEqual(events[0].findtext("args/arg"), "a b")
        self.assertTrue(events[0].findtext("datetime"))
        self.assertEqual(events[1].findtext("status"), "error")


if __name__ == "__main__":
    unittest.main()
