#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f $DIR/docker-compose.yml ] || [ -f $DIR/compose.yml ]; then
    echo "Starting Docker Compose..."
    # docker compose build --no-cache
    docker compose up -d --build 
    if [ $? -eq 0 ]; then
        echo "Docker Compose has been built and started!"
    else
        echo "Docker Compose failed!"
        exit 1
    fi
else
    echo "Docker Compose file not found!"
fi
