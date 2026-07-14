#!/bin/bash

set -e
BASE_URL=$1
echo "Running smoke tests"

curl --fail "$BASE_URL/"

curl --fail "$BASE_URL/health"

echo "Smoke tests passed"
