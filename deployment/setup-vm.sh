#!/bin/bash

# Exit if a command fails
set -e

# Update Ubuntu package list
echo "Updating package list..."
sudo apt update

# Install deployment dependencies
echo "Installing Docker and supporting tools..."
sudo apt install -y docker.io docker-compose-v2 curl git

# Start and enable Docker
echo "Starting Docker..."
sudo systemctl enable --now docker

# Verify Docker installation
echo "Checking Docker version..."
sudo docker --version

# Verify Docker Compose installation
echo "Checking Docker Compose version..."
sudo docker compose version

# Test Docker with a sample container
echo "Testing Docker installation..."
sudo docker run --rm hello-world

echo "Virtual machine setup completed successfully."
