#!/bin/bash

set -e

echo "Deploying Nginx test website..."

# Check whether the container already exists
if sudo docker container inspect test-website >/dev/null 2>&1; then
    sudo docker start test-website
else
    sudo docker run -d \
        --name test-website \
        -p 80:80 \
        nginx:alpine
fi

echo "Checking running containers..."
sudo docker ps

echo "Testing website connectivity..."
curl --fail --retry 5 --retry-connrefused \
    http://localhost

echo "Website deployment successful!"
