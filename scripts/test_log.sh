#!/bin/bash
# Только лог: введите несколько команд, затем откройте log.xml.
cd "$(dirname "$0")/.." || exit 1
./run.sh --log ./log.xml
