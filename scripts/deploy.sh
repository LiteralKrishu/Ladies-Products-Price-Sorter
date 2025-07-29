#!/bin/bash

echo "=== Deploying Ladies Product Price Sorter ==="

# Load environment variables
if [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
else
    echo "Warning: .env file not found"
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r ../requirements.txt

# Run tests
echo "Running tests..."
cd ../backend && python -m pytest -v && cd -

# Start the service
echo "Starting FastAPI server..."
uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --proxy-headers \
    --timeout-keep-alive 60