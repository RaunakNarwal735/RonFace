@echo off
REM Create virtual environment in 'venv' directory
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install required packages
pip install -r requirements.txt

echo Virtual environment setup complete. To activate later, run:
echo   venv\Scripts\activate.bat 