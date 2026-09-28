#!/bin/bash

set -e

GRID_JAR="grid/selenium-server-4.33.0.jar"

java -jar "$GRID_JAR" hub &
HUB_PID=$!
java -jar "$GRID_JAR" node --hub http://localhost:4444 &
NODE_PID=$!
trap 'kill $HUB_PID $NODE_PID' EXIT

for _ in $(seq 1 30); do
    if curl -sf http://localhost:4444/status > /dev/null; then
        break
    fi
    sleep 2
done

GRID="true" BROWSERS="${1:-}" pytest -n "${2:-auto}" --reruns 2 --alluredir=allure-results
