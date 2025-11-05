#!/bin/bash
set -e
# some basic setup for the project. Exist for convenience.
echo "SETUP WIZ"
echo "Installing project dependencies"
pip install -r requirements.txt
echo "Making migrations..."
python manage.py makemigrations --settings=mysite.settings.production
echo "Done..."
echo "Running Migrations..."
python manage.py migrate --settings=mysite.settings.production
echo "Done..."
echo "Setting up static files, running Collectstatic.."
python manage.py collectstatic --settings=mysite.settings.production --no-input
echo "Done..."
echo "Create Super User"
python manage.py createsuperuser --settings=mysite.settings.production
echo "Done..."
echo "Setup finished!"




