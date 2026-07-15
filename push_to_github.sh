#!/bin/bash

# SBTU MCP Server - Push Automation Utility
# This script automates staging, committing, and pushing changes securely to GitHub.

# Set error handling
set -e

echo "=========================================="
echo "🚀 SBTU MCP Server Push Automation"
echo "=========================================="

# Check if logged in to gh CLI
if ! gh auth status &>/dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not authenticated. Please run 'gh auth login' first."
    exit 1
fi

# Ensure user name and email are configured
if [ -z "$(git config user.name)" ]; then
    echo "ℹ️ Configuring local git user name..."
    git config --local user.name "remixms029g"
fi
if [ -z "$(git config user.email)" ]; then
    echo "ℹ️ Configuring local git user email..."
    git config --local user.email "remixms029g@users.noreply.github.com"
fi

# Get commit message from argument
COMMIT_MSG="$1"
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="chore: update repository files"
fi

echo "📦 Staging all files..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "✓ No changes to commit (working directory is clean)."
else
    echo "💾 Committing changes: \"$COMMIT_MSG\"..."
    git commit -m "$COMMIT_MSG"
fi

echo "🔐 Retrieving GitHub auth token..."
TOKEN=$(gh auth token)

if [ -z "$TOKEN" ]; then
    echo "❌ Error: Failed to retrieve active auth token from GitHub CLI."
    exit 1
fi

echo "☁️ Pushing updates to origin main..."
git push https://x-access-token:${TOKEN}@github.com/remixms029g/sbtu-mcp-server.git main

echo "=========================================="
echo "🎉 Update successfully pushed to GitHub!"
echo "=========================================="
