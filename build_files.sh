#!/bin/bash
# Build script for Vercel
echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

