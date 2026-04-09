#!/bin/bash

URL="http://localhost:8081/overview"

echo "⏳ Waiting for Flink JobManager to be ready at $URL..."

while true; do
    RESPONSE=$(curl -s $URL)
    if [ $? -eq 0 ]; then
        TM_COUNT=$(echo $RESPONSE | grep -o '"taskmanagers":[0-9]*' | cut -d: -f2)
        if [ "$TM_COUNT" -gt 0 ]; then
            echo -e "\n✅ Flink is up with $TM_COUNT TaskManager(s)!"
            break
        fi
    fi
    printf "."
    sleep 2
done

echo -e "\n✅ Flink is up and running!"
