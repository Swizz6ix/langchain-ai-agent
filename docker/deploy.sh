#!/bin/bash

set -e

echo "Starting deployment"

IMAGE_NAME=$1
IMAGE_TAG=$2
HEALTH_URL=$3
BASE_URL=$4

if [ -z "$IMAGE_NAME"] || [ -z "IMAGE_TAG" ]; then
    echo "Missing image information"
    exit 1
fi

echo "Current container"

docker compose ps


echo "Saving current version"

CURRENT_IMAGE=$(docker inspect langchain-agent \
--format='{{.Config.Image}}' 2>/dev/null || true)

if [! -z "$CURRENT_IMAGE" ]; then
    echo $CURRENT_IMAGE > previous_image.txt
fi


echo "Pulling new image"

export IMAGE_NAME
export IMAGE_TAG


docker compose pull

echo "Starting new version"


docker compose up -d

echo "Waiting for health"

sleep 15

curl --fail http://localhost:8000/health

echo "Running health check"

./health-check.sh "$HEALTH_URL"


echo "Running smoke tests"

./smoke-test.sh "$BASE_URL

echo "Deployment successful"
