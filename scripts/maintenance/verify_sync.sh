#!/bin/bash

# Git Sync Verification Script
# This script checks if the local repository is in sync with GitHub and the Redmine mirror.

LOCAL_HEAD=$(git rev-parse HEAD)
GITHUB_URL="git@github.com:NkgoloL/edo-boost-main.git"
REDMINE_PATH="/opt/repo/edo-boost-main.git"

echo "Local HEAD: $LOCAL_HEAD"

echo "Checking GitHub..."
# Note: This might prompt for passphrase if not in ssh-agent
REMOTE_GITHUB=$(git ls-remote "$GITHUB_URL" refs/heads/main | awk '{print $1}')
if [ "$LOCAL_HEAD" == "$REMOTE_GITHUB" ]; then
    echo "[OK] GitHub is in sync with local main."
else
    echo "[FAIL] GitHub is NOT in sync!"
    echo "  GitHub main: $REMOTE_GITHUB"
    echo "  Local main:  $LOCAL_HEAD"
fi

echo "Checking Redmine Mirror..."
if [ -d "$REDMINE_PATH" ]; then
    REMOTE_REDMINE=$(git --git-dir="$REDMINE_PATH" rev-parse main)
    if [ "$LOCAL_HEAD" == "$REMOTE_REDMINE" ]; then
        echo "[OK] Redmine mirror is in sync."
    else
        echo "[FAIL] Redmine mirror is NOT in sync!"
        echo "  Redmine main: $REMOTE_REDMINE"
    fi
else
    echo "[SKIP] Redmine path $REDMINE_PATH not found or inaccessible."
fi

echo "--- Suggestion ---"
echo "If GitHub is out of sync, try running: git push origin main --verbose"
echo "Check for any errors during the push to the GitHub URL."
