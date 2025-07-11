#!/bin/bash

# Exit on any error
set -e

# Activate the virtual environment
source "$(dirname "$0")/../.venv/bin/activate"

# Navigate to project root
cd "$(dirname "$0")/.."

# Log file
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Run management command and capture output
DELETED_OUTPUT=$(python3 manage.py delete_old_customers)

# Log the output with timestamp
echo "$(date): $DELETED_OUTPUT" >> "$LOG_FILE"
