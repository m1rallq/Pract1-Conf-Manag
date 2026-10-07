"""Логирование вызовов команд в файл формата XML."""

import xml.etree.ElementTree as element_tree
from datetime import datetime


class XmlLogger:
    """Записывает события вызова команд в XML-файл.

    Каждое событие содержит дату и время, имя команды, аргументы
    и статус выполнения. Файл перезаписывается после каждого
    события, поэтому он всегда остаётся корректным XML.
    """

    def __init__(self, path):
        """Создаёт логгер. Если path пустой, логирование отключено."""
        self.path = path
        self.root = element_tree.Element("log")

    def log(self, command, args, status, message=""):
        """Добавляет событие вызова команды и сохраняет файл."""
        if not self.path:
            return
        event = element_tree.SubElement(self.root, "event")
        element_tree.SubElement(event, "datetime").text = (
            datetime.now().isoformat(timespec="seconds")
        )
        element_tree.SubElement(event, "command").text = command
        args_node = element_tree.SubElement(event, "args")
        for arg in args:
            element_tree.SubElement(args_node, "arg").text = arg
        element_tree.SubElement(event, "status").text = status
        if message:
            element_tree.SubElement(event, "message").text = message
        self._save()

    def _save(self):
        """Сохраняет накопленные события в файл."""
        tree = element_tree.ElementTree(self.root)
        element_tree.indent(tree)
        tree.write(self.path, encoding="utf-8", xml_declaration=True)
