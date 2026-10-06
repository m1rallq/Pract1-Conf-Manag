"""Параметры эмулятора, задаваемые из командной строки."""

import argparse
import os
from dataclasses import dataclass
from typing import Optional

DEFAULT_VFS_NAME = "vfs"


@dataclass
class Config:
    """Настройки эмулятора.

    Attributes:
        vfs_path: путь к физическому расположению VFS.
        log_path: путь к XML-файлу лога.
        script_path: путь к стартовому скрипту.
    """

    vfs_path: Optional[str] = None
    log_path: Optional[str] = None
    script_path: Optional[str] = None

    @property
    def vfs_name(self):
        """Имя VFS для заголовка окна (последняя часть пути)."""
        if not self.vfs_path:
            return DEFAULT_VFS_NAME
        name = os.path.basename(os.path.normpath(self.vfs_path))
        return name or DEFAULT_VFS_NAME

    def as_pairs(self):
        """Возвращает параметры как список пар (ключ, значение)."""
        return [
            ("vfs", self.vfs_path or ""),
            ("vfs_name", self.vfs_name),
            ("log", self.log_path or ""),
            ("script", self.script_path or ""),
        ]

    def dump(self):
        """Возвращает параметры в формате ``ключ=значение`` по строкам."""
        return "\n".join(f"{key}={value}" for key, value in self.as_pairs())


def build_arg_parser():
    """Создаёт разборщик аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки UNIX с VFS",
    )
    parser.add_argument("--vfs", dest="vfs_path",
                        help="путь к физическому расположению VFS")
    parser.add_argument("--log", dest="log_path",
                        help="путь к лог-файлу (XML)")
    parser.add_argument("--script", dest="script_path",
                        help="путь к стартовому скрипту")
    return parser


def parse_args(argv=None):
    """Разбирает аргументы командной строки и возвращает Config."""
    namespace = build_arg_parser().parse_args(argv)
    return Config(
        vfs_path=namespace.vfs_path,
        log_path=namespace.log_path,
        script_path=namespace.script_path,
    )
