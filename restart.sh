#!/bin/bash

IMAGE="2023ac05602/iris-api:latest"
CONTAINER_NAME="iris-api-container"

# Stop and remove any existing container
podman stop $CONTAINER_NAME 2>/dev/null && podman rm $CONTAINER_NAME 2>/dev/null

# Pull latest image
podman pull $IMAGE

# Start container and mount logs directory
podman run -d -p 5000:5000 --name $CONTAINER_NAME -v ./logs:/app/logs $IMAGE

echo "🚀 API is now running at http://localhost:5000"