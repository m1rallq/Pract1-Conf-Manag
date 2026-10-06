#!/bin/bash
# Все параметры сразу: VFS, лог и стартовый скрипт.
cd "$(dirname "$0")/.." || exit 1
./run.sh --vfs ./myvfs --log ./log.xml --script scripts/start_ok.txt
