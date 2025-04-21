#!/bin/bash
cd /home/brokkoli/GITHUB/sideproject-management
source /home/brokkoli/GITHUB/sideproject-management/.venv/bin/activate
exec python manage.py runserver 0.0.0.0:8000 \
  >> /home/brokkoli/GITHUB/sideproject-management/app.log 2>&1

