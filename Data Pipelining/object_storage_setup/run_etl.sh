#!/bin/bash
set -e

# Navigate to your project directory on the instance
cd ~/Vision-to-Vintage-AIs-Take-on-Classical-Art

# Define the docker compose file path
COMPOSE_FILE="Data Pipelining/docker/docker-compose-etl.yaml"

# Set the RCLONE container name (⚠️ REPLACE with your NetID)
export RCLONE_CONTAINER=object-persist-<yourNetID>

echo "[1/3] Running Extract Stage..."
docker compose -f "$COMPOSE_FILE" run extract-data

echo "[2/3] Running Transform Stage..."
docker compose -f "$COMPOSE_FILE" run transform-data

echo "[3/3] Running Load Stage..."
docker compose -f "$COMPOSE_FILE" run load-data

echo "ETL Pipeline complete!"
