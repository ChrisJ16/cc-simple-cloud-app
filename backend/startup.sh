#!/bin/bash

echo "Current directory: $(pwd)"
echo "Files:"
ls -la

pip install -r requirements.txt

gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
