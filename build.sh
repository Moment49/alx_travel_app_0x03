#!/usr/bin/env bash

set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python alx_travel_app/manage.py collectstatic --noinput

echo "Applying database migrations..."
python alx_travel_app/manage.py migrate
