#!/usr/bin/env bash
set -e

# создаём постоянный каталог для Dockge, если его нет
mkdir -p /data/addons_config/dockge/data

# удаляем локальную ./data и создаём симлинк на постоянный каталог
rm -rf /app/data
ln -s /data/addons_config/dockge/data /app/data

# запускаем оригинальный CMD
exec "$@"
