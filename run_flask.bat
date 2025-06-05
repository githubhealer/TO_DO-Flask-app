@echo off
cd /d D:\TIMETABLE\TO_DO-Flask-app
set FLASK_APP=app.py
set FLASK_ENV=development
python -m flask run
pause