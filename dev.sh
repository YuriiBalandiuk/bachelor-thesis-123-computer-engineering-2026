#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f $DIR/docker-compose.yml ] || [ -f $DIR/compose.yml ]; then
    echo "Starting Docker Compose..."
    # docker compose build --no-cache
    if [ $? -eq 0 ]; then
        docker compose up -d --build 
        echo "Docker Compose has been built and started!"
    else
        echo "Docker Compose failed!"
        exit 1
    fi
else
    echo "Docker Compose file not found!"
fi
