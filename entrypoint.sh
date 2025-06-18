#!/bin/bash

set -e

if [ ! -d "$PROJECT_NAME" ]; then
    echo "✅ Creating Project Folder"
    mkdir "$PROJECT_NAME"
    echo "👉 Access Project Folder"
    cd $PROJECT_NAME
    echo "🔵 Creating TOML files"
    poetry init --name "$PROJECT_NAME" --no-interaction
else
    echo "👉 Access Project Folder"
    cd $PROJECT_NAME
fi

poetry install --no-root

if [ ! -d ".venv" ]; then
    echo "🆙 Install dependencies"
    poetry add django
    poetry add psycopg2-binary
fi

if [ ! -f "manage.py" ]; then
    echo "🏛️ Creating Django Project"
    poetry run django-admin startproject config .
fi

if [ -z "$1" ]; then
    echo "🚀 Running Server [0.0.0.0:$PORT]"
    exec poetry run python manage.py runserver 0.0.0.0:$PORT
else
    echo "🤖 Running Command"
    exec "$@"
fi
