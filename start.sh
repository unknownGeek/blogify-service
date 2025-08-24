#!/bin/bash
# Startup script for running the Flask blog API

# Activate virtual environment if exists
test -d venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
export FLASK_APP=server.py
export FLASK_ENV=development
flask run --port=3000
