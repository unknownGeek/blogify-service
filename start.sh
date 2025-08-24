#!/bin/bash
# Startup script for running the Flask blog API

# Activate virtual environment if exists
test -d venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python server.py 