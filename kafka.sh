#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f $DIR/docker-compose.yml ] || [ -f $DIR/compose.yml ]; then
    echo "Starting configuration Kafka Cluster..."
    
    docker exec -it kafka1 kafka-topics \
        --create \
        --topic thingspeak-topic \
        --bootstrap-server kafka1:9092 \
        --replication-factor 2 \
        --partitions 2 \
        --config retention.ms=604800000 \
        --config retention.bytes=3221225472
        
        # Store for 7 days and store up to 3 GB

    if [ $? -eq 0 ]; then
        echo "Kafka Topic has been created!"
    else
        echo "Kafka Topic creation has failed!"
        exit 1
    fi
else
    echo "Docker Compose file not found!"
fi