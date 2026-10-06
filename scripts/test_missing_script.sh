#!/bin/bash
# Несуществующий стартовый скрипт: эмулятор сообщит об ошибке.
cd "$(dirname "$0")/.." || exit 1
./run.sh --script scripts/no_such_file.txt
