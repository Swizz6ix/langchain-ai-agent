#!/bin/bash

set -e

if [ ! -f previous_image.txt ]; then

    echo "No previous version found"
    exit 1
fi


PREVIOUS_IMAGE=$(cat previous_image.txt)

echo "Rolling back to:"
echo $PREVIOUS_IMAGE


export IMAGE_NAME=$(echo $PREVIOUS_IMAGE | cut -d: -f1)
export IMAGE_TAG=$(echo $PREVIOUS_IMAGE | cut -d: -f2)


docker compose down
docker compose up -d

echo "Rollback completed"