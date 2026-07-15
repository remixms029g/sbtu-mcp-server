#!/bin/bash
git add .
git commit -m "chore: make repository production-ready with MCP server config, Dockerfile, and README updates"
TOKEN=$(gh auth token)
git push https://x-access-token:${TOKEN}@github.com/remixms029g/sbtu-mcp-server.git main
