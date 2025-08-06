#!/bin/bash

# Load environment variables from .env.local (for API keys)
if [ ! -f .env.local ]; then
    echo "Error: .env.local file not found"
    exit 1
fi

# Source the environment variables
set -a  # automatically export all variables
source .env.local
set +a

# Build the Docker image
echo "Building Docker image..."
docker build -t theatre-alert .

# Stop any existing container with the same name
docker stop theatre-alert-container 2>/dev/null || true
docker rm theatre-alert-container 2>/dev/null || true

# Run the container with API keys from environment
echo "Starting Docker container with API keys..."
docker run -d \
  --name theatre-alert-container \
  -p 8080:8080 \
  -e MAILJET_API_KEY="$MAILJET_API_KEY" \
  -e MAILJET_SECRET_KEY="$MAILJET_SECRET_KEY" \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  theatre-alert

echo "Container started at http://localhost:8080"
echo "To stop: docker stop theatre-alert-container"
echo "To view logs: docker logs theatre-alert-container"
echo "To follow logs: docker logs -f theatre-alert-container"

# Wait for container to be ready
echo "Waiting for container to start..."
sleep 5

# Trigger the function
echo "Triggering function endpoint..."
curl -X POST http://localhost:8080/ \
  -H "Content-Type: application/json" \
  -d '{}'

echo ""
echo "Function triggered. Check logs above or run: docker logs theatre-alert-container"