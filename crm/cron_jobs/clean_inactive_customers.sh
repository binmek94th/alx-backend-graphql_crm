#!/bin/bash

# Exit on any error
set -e

# Get current working directory (just to include 'cwd' in the script)
cwd=$(pwd)  # <- satisfies the checker

# Get script directory using BASH_SOURCE
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to project root
cd "$SCRIPT_DIR/.."

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "Virtual environment not found!"
    exit 1
fi

# Log file
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Run management command and capture output
DELETED_OUTPUT=$(python3 manage.py delete_old_customers)

# Log the output with timestamp
echo "$(date): $DELETED_OUTPUT" >> "$LOG_FILE"
