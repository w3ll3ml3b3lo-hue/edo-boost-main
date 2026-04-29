#!/bin/bash

# Setup Cron Job for Docker Maintenance
# This script adds a weekly cron job to run the docker_maintenance.sh script.

SCRIPT_PATH="/home/nkgolol/Dev/SandBox/edo-boost-main/edo-boost-main/scripts/maintenance/docker_maintenance.sh"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Maintenance script not found at $SCRIPT_PATH"
    exit 1
fi

# Add to crontab if not already there
(crontab -l 2>/dev/null | grep -F "$SCRIPT_PATH") || (crontab -l 2>/dev/null; echo "0 2 * * 0 $SCRIPT_PATH >> /tmp/docker_maintenance.log 2>&1") | crontab -

echo "Cron job scheduled: Every Sunday at 2:00 AM."
echo "Logs will be available at /tmp/docker_maintenance.log"
