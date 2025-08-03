#!/bin/bash

IMAGE="2023ac05602/iris-api:latest"
CONTAINER_NAME="iris-api-container"
HOST_LOG_DIR="./logs"
CONTAINER_LOG_DIR="/app/logs"

# Ensure log directory exists
mkdir -p $HOST_LOG_DIR

# Stop and remove any existing container
podman stop $CONTAINER_NAME 2>/dev/null && podman rm $CONTAINER_NAME 2>/dev/null

# Pull the latest image from Docker Hub
podman pull $IMAGE

# Run the container with log directory mounted
podman run -d \
  -p 5000:5000 \
  --name $CONTAINER_NAME \
  -v "$HOST_LOG_DIR:$CONTAINER_LOG_DIR" \
  $IMAGE

echo "🚀 API is now running at http://localhost:5000"
echo "📄 Logs will be written to $HOST_LOG_DIR/iris_api.log"
