@echo off
title Ortho4XPDark Installation Helper

echo.
echo ================================
echo Ortho4XPDark Installation Helper
echo ================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.8+ and try again
    echo.
    pause
    exit /b 1
)

echo Starting guided installation...
echo.

REM Run the Python installation helper
python install_dependencies.py

echo.
echo Installation helper finished.
echo.
pause
