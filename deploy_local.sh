#!/bin/bash

IMAGE="2023ac05602/iris-api:latest"
CONTAINER_NAME="iris-api-container"
HOST_LOG_DIR="./app/logs"
CONTAINER_LOG_DIR="/app/logs"

# Stop and remove existing container
podman stop $CONTAINER_NAME 2>/dev/null && podman rm $CONTAINER_NAME 2>/dev/null

# Ensure local log directory exists
mkdir -p $HOST_LOG_DIR

# Build the latest Docker image
echo "Building Docker image"
podman build -t $IMAGE .

# Pull the latest image from Docker Hub (optional if pushing from another machine)
# podman pull $IMAGE

# Run container with volume mount for logs
echo " Starting container..."
podman run -d \
  -p 5000:5000 \
  --name $CONTAINER_NAME \
  -v "$(pwd)/app/logs":$CONTAINER_LOG_DIR \
  $IMAGE

echo "Container '$CONTAINER_NAME' is running."
echo "API available at: http://localhost:5000"
echo "Logs will be written to: $HOST_LOG_DIR/iris_api.log"
