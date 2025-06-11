#!/bin/bash

MAIN="../src/5ka_warehouse/main.py"

if [ ! -f "$MAIN" ]; then
    echo "Error: Main script not found at $MAIN"
    exit 1
fi


poetry run python3 "$MAIN"