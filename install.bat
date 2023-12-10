@echo off
pip install -r requirements.txt
echo.
echo Installation complete.

REM Run the Python script
python main.py

echo.
echo Press any key to exit...
pause >nul
