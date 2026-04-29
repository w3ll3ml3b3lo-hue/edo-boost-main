#!/bin/bash
# EduBoost SA — Docker Maintenance Script
# Systematically prunes unused Docker resources to prevent disk exhaustion.

echo "--- Starting Docker Cleanup: $(date) ---"

# 1. Prune unused images, containers, networks (dangling ones)
docker system prune -f

# 2. Prune build cache (can grow very large)
docker builder prune -f --all

# 3. Prune unused volumes (be careful: only prunes volumes NOT used by any container)
docker volume prune -f

echo "--- Cleanup Complete ---"
docker system df
