@echo off

REM Set the path to your virtual environment activate script
set "VENV_PATH=C:\path\to\your\virtual\environment\Scripts\activate.bat"

REM Change to the directory containing your Flask app
cd /home/asmaa/sample_flask_app

REM Activate the virtual environment
call %VENV_PATH%

REM Run your Flask app
python app.py
