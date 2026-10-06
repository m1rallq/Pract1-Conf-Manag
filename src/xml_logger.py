"""Логирование вызовов команд в файл формата XML."""

import xml.etree.ElementTree as ET
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
        self.root = ET.Element("log")

    def log(self, command, args, status, message=""):
        """Добавляет событие вызова команды и сохраняет файл."""
        if not self.path:
            return
        event = ET.SubElement(self.root, "event")
        ET.SubElement(event, "datetime").text = (
            datetime.now().isoformat(timespec="seconds")
        )
        ET.SubElement(event, "command").text = command
        args_node = ET.SubElement(event, "args")
        for arg in args:
            ET.SubElement(args_node, "arg").text = arg
        ET.SubElement(event, "status").text = status
        if message:
            ET.SubElement(event, "message").text = message
        self._save()

    def _save(self):
        """Сохраняет накопленные события в файл."""
        tree = ET.ElementTree(self.root)
        ET.indent(tree)
        tree.write(self.path, encoding="utf-8", xml_declaration=True)
