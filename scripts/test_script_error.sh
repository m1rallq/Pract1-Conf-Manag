#!/bin/bash
# Стартовый скрипт с ошибкой: эмулятор сообщит номер строки.
cd "$(dirname "$0")/.." || exit 1
./run.sh --vfs ./myvfs --script scripts/start_error.txt
