#!/bin/bash
# Скрипт с командой exit: окно закроется само, код выхода 0.
cd "$(dirname "$0")/.." || exit 1
./run.sh --log ./log.xml --script scripts/start_exit.txt
echo "Эмулятор завершился с кодом $?"
