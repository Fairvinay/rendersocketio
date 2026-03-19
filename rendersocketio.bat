@echo off
:: ==================================================
:: Step 0: Check & Relaunch as Administrator if needed
:: ==================================================
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

:: ==================================================
:: Step 1: Kill Python process on port 9384
:: ==================================================
echo Checking for Python process on port 9384...
FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :9384') DO (
    echo Killing process ID %%P ...
    taskkill /PID %%P /F
)

:: ==================================================
:: Step 2: Change to project directory
:: ==================================================
cd /d C:\icici\rendersocketio

:: ==================================================
:: Step 3: Create virtual environment if not exists
:: ==================================================
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: ==================================================
:: Step 4: Activate virtual environment
:: ==================================================
call venv\Scripts\activate

:: ==================================================
:: Step 5: Run the Flask CORS
:: ==================================================
echo installing flask cors ...
echo Checking if flask-cors is installed...
python -m pip show flask-cors >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing flask-cors...
    python -m pip install flask-cors
) else (
    echo flask-cors is already installed. Skipping install.
)

:: ==================================================
:: Step 6: Run the Python program
:: ==================================================
echo Starting app.py ...
python app.py

:: ==================================================
:: Step 7: Pause before exit
:: ==================================================
pause
