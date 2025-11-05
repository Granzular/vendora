#!/bin/bash
# Runs collectstatic
python manage.py collectstatic --settings=mysite.settings.production --no-input
