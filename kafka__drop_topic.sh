#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f $DIR/docker-compose.yml ] || [ -f $DIR/compose.yml ]; then
    echo "Deleting topic in Kafka Cluster..."
    
    docker exec -it kafka1 kafka-topics \
        --delete \
        --topic test-1-topic \
        --bootstrap-server kafka1:9092

    if [ $? -eq 0 ]; then
        echo "Kafka Topic has been deleted!"
    else
        echo "Kafka Topic deletion has failed!"
        exit 1
    fi
else
    echo "Docker Compose file not found!"
fi