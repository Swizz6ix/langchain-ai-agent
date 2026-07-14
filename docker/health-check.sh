#!/bin/bash

set -e
URL=$1

if [ -z "$URL" ]; then
    echo "Health URL missing"
    exit 1
fi

echo "Checking application health..."

for i in {1..10}
do

    if curl --fail --silent "$URL/health"; then
        echo "Health check passed"
        exit 0
    fi

    echo "Waiting for application..."
    sleep 5
done


echo "Health check failed"

exit 1
