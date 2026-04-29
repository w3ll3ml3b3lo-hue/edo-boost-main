#!/bin/bash

# Docker Maintenance Script
# This script cleans up unused Docker resources to free up disk space.

set -e

echo "--- Starting Docker Maintenance ---"
date

# 1. Remove dangling images, containers, and networks
echo "Cleaning up dangling resources..."
docker system prune -f

# 2. Remove unused volumes (Be careful: this removes volumes not used by any container)
echo "Cleaning up unused volumes..."
docker volume prune -f

# 3. Remove unused images (including non-dangling ones that are not used by containers)
# We keep images from the last 7 days to avoid re-downloading everything constantly.
echo "Cleaning up old unused images..."
docker image prune -a -f --filter "until=168h"

# 4. Clean up build cache
echo "Cleaning up build cache..."
docker builder prune -f

echo "--- Current Docker Disk Usage ---"
docker system df

echo "--- Maintenance Complete ---"
