#!/bin/bash

# Standardized Docker Compose wrapper for BMAD Agent Stacks.
# This ensures that all developer commands are executed within the 
# correct Docker context.

# Check if docker compose is available
if ! command -v docker &> /dev/null
then
    echo "Error: 'docker' command not found. Please install Docker."
    exit 1
fi

# Proxy all arguments to docker compose
docker compose "$@"
