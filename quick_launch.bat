@echo off
title Ortho4XPDark - Quick Launch

echo.
echo 🌑 Ortho4XPDark - Dark Theme for Ortho4XP
echo ==========================================
echo.
echo This is a hobbyist dark theme modification for Ortho4XP.
echo.
echo 🧪 Testing what actually works first...
echo.

REM Test Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found - please install Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python available
echo.

REM Test basic functionality
echo 🧪 Testing tkinter (for dark theme)...
python -c "import tkinter; print('✅ Dark theme should work')" 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ Tkinter issue - dark theme may not work
    set DARK_OK=false
) else (
    echo ✅ Dark theme ready
    set DARK_OK=true
)

REM Test XRoads dependencies
echo 🧪 Testing XRoads dependencies (shapely)...
python -c "import shapely; print('✅ XRoads ready')" 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ XRoads needs dependencies (run: pip install -r requirements.txt)
    set XROADS_OK=false
) else (
    echo ✅ XRoads ready
    set XROADS_OK=true
)

echo.
echo 📋 WHAT WORKS:
echo.

if "%DARK_OK%"=="true" (
    echo ✅ [1] Dark Theme - Ready
) else (
    echo ❌ [1] Dark Theme - Needs fixing
)

if "%XROADS_OK%"=="true" (
    echo ✅ [2] XRoads Transparent Roads - Ready
) else (
    echo ❌ [2] XRoads - Needs dependencies
)

echo ✅ [3] System Check - Ready
echo ✅ [4] Main Launcher - Ready
echo 🔧 [5] Install Missing Stuff

echo.
set /p choice="Pick what to try (1-5): "

if "%choice%"=="1" (
    if "%DARK_OK%"=="true" (
        echo Starting dark theme...
        python Ortho4XPDark.py
    ) else (
        echo Dark theme might not work, trying anyway...
        python Ortho4XPDark.py
    )
) else if "%choice%"=="2" (
    if "%XROADS_OK%"=="true" (
        echo Testing XRoads...
        python test_xroads.py
    ) else (
        echo XRoads needs dependencies first. Install them?
        echo Running: pip install -r requirements.txt
        pip install -r requirements.txt
        echo Now try: python test_xroads.py
        pause
    )
) else if "%choice%"=="3" (
    echo Running system check...
    python system_verification.py
) else if "%choice%"=="4" (
    echo Starting main launcher...
    python enhanced_launcher.py
) else if "%choice%"=="5" (
    echo Installing dependencies for full functionality...
    pip install -r requirements.txt
    echo.
    if %ERRORLEVEL% equ 0 (
        echo ✅ Done! Now XRoads and other features should work.
    ) else (
        echo ❌ Install failed. Check GDAL_INSTALLATION.md for help.
    )
    pause
) else (
    echo Starting main launcher...
    python enhanced_launcher.py
)

echo.
echo Done. This is just a hobbyist modification to make Ortho4XP dark-themed.
pause
