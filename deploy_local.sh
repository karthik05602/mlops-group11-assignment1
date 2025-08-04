#!/bin/bash

IMAGE="2023ac05602/iris-api:latest"
CONTAINER_NAME="iris-api-container"
HOST_LOG_DIR="./app/logs"
CONTAINER_LOG_DIR="/app/logs"
HOST_DATA_DIR="./data"
CONTAINER_DATA_DIR="/data"

# Stop and remove existing container
podman stop $CONTAINER_NAME 2>/dev/null && podman rm $CONTAINER_NAME 2>/dev/null

# Ensure local log and data directories exist
mkdir -p $HOST_LOG_DIR
mkdir -p $HOST_DATA_DIR

# Build the image (optional, include only if you're building before running)
podman build -t $IMAGE .

# Pull the latest image
podman pull $IMAGE

# Run container with volume mounts for logs and data
podman run -d \
  -p 5000:5000 \
  --name $CONTAINER_NAME \
  -v "$(pwd)/app/logs":$CONTAINER_LOG_DIR \
  -v "$(pwd)/data":$CONTAINER_DATA_DIR \
  $IMAGE

echo "API is running at http://localhost:5000"
echo "Logs: $HOST_LOG_DIR/iris_api.log"
echo "Data available inside container at /data"
