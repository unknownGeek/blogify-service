#!/bin/bash
# Startup script for running the Flask blog API

# Activate virtual environment if exists
test -d venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

export API_URL=http://localhost:5000/api
# Run the Flask server
python server.py 