#!/usr/bin/env bash

set -Eeuo pipefail

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}


# Validate Arguments
if [[ $# -ne 4 ]]; then
    echo "Usage:"
    echo "./deploy.sh <image_name> <image_tag> <health_url> <base_url>"
    exit 1
fi

IMAGE_NAME="$1"
IMAGE_TAG="$2"
HEALTH_URL="$3"
BASE_URL="$4"


# Configuration
COMPOSE_FILE="docker-compose.yml"
CONTAINER_NAME="langchain-agent"

ROLLBACK_FILE=".previous_image"


# Rollback Function
rollback() {

    log "Rolling back deployment..."

    if [[ ! -f "$ROLLBACK_FILE" ]]; then
        log "No rollback information found."
        exit 1
    fi

    PREVIOUS_IMAGE=$(cat "$ROLLBACK_FILE")

    export IMAGE_NAME="${PREVIOUS_IMAGE%:*}"
    export IMAGE_TAG="${PREVIOUS_IMAGE##*:}"

    docker compose -f "$COMPOSE_FILE" up -d

    log "Rollback completed."

    exit 1
}


# Rollback on Unexpected Failure
trap rollback ERR


# Save Current Deployment
log "Saving current deployment..."

CURRENT_IMAGE=$(docker inspect "$CONTAINER_NAME" \
    --format='{{.Config.Image}}' 2>/dev/null || true)

if [[ -n "$CURRENT_IMAGE" ]]; then
    echo "$CURRENT_IMAGE" > "$ROLLBACK_FILE"
    log "Current image: $CURRENT_IMAGE"
else
    log "No existing deployment found."
fi


# Deploy New Version
export IMAGE_NAME
export IMAGE_TAG

log "Pulling image..."

docker compose -f "$COMPOSE_FILE" pull

log "Starting containers..."

docker compose -f "$COMPOSE_FILE" up -d --remove-orphans


# Wait for Health
log "Waiting for application..."

HEALTHY=false

for i in {1..30}; do

    if curl -fsS "$HEALTH_URL" >/dev/null; then
        HEALTHY=true
        break
    fi

    sleep 5

done

if [[ "$HEALTHY" != true ]]; then
    log "Health check failed."
    rollback
fi

log "Health check passed."

# Run Additional Health Checks
if [[ -x "./health-check.sh" ]]; then

    log "Running health checks..."

    ./health-check.sh "$HEALTH_URL"

fi


# Smoke Tests
if [[ -x "./smoke-test.sh" ]]; then

    log "Running smoke tests..."

    ./smoke-test.sh "$BASE_URL"

fi


# Cleanup
log "Cleaning unused Docker images..."

docker image prune -f >/dev/null || true


# Deployment Complete
rm -f "$ROLLBACK_FILE"

log "Deployment completed successfully."

docker compose ps
