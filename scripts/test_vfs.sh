#!/bin/bash
# Только путь к VFS: имя VFS должно появиться в заголовке окна.
cd "$(dirname "$0")/.." || exit 1
./run.sh --vfs "/home/user/my vfs"
