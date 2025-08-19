@echo off
title Ortho4XPDark - Dark Theme Mod for Ortho4XP

:start
echo.
echo 🌑 Ortho4XPDark - Dark Theme Mod for Ortho4XP
echo ==============================================
echo.
echo This is a hobbyist modification to add dark theme to Ortho4XP.
echo Also includes some other enhancements I've been working on.
echo.
echo Choose what to try:
echo.
echo [1] 🚀 Main Launcher
echo     All the tools in one place
echo.
echo [2] 🌑 Dark Theme Only
echo     Just the dark-themed Ortho4XP
echo.
echo [3] 🌲 Forest Manager
echo     Manage treelines (needs dependencies)
echo.
echo [4] 🔍 System Check
echo     See what's working on your system
echo.
echo [5] 🛣️  XRoads Testing
echo     Test melbo's transparent roads (needs dependencies)
echo.
echo [6] 📦 Install Dependencies
echo     Install packages for full functionality
echo.
echo [7] 📖 Read Documentation
echo     Open README file
echo.
echo [8] 🧪 Quick Test
echo     Check what works without failing
echo.
set /p choice="Pick option (1-8): "

if "%choice%"=="1" (
    echo.
    echo Starting main launcher...
    python enhanced_launcher.py
) else if "%choice%"=="2" (
    echo.
    echo Starting dark theme...
    python Ortho4XPDark.py
) else if "%choice%"=="3" (
    echo.
    echo Starting forest manager...
    echo (May need dependencies - see option 6 if it fails)
    python treelines_manager.py
) else if "%choice%"=="4" (
    echo.
    echo Running system check...
    python system_verification.py
) else if "%choice%"=="5" (
    echo.
    echo Testing XRoads...
    echo (May need dependencies - see option 6 if it fails)
    python test_xroads.py
) else if "%choice%"=="6" (
    echo.
    echo Installing dependencies...
    echo This installs packages needed for XRoads and other features.
    echo.
    pip install -r requirements.txt
    echo.
    if %ERRORLEVEL% equ 0 (
        echo ✅ Done! Features should work now.
    ) else (
        echo ❌ Install failed. Check GDAL_INSTALLATION.md for help.
    )
    echo.
    pause
    goto start
) else if "%choice%"=="7" (
    echo.
    echo Opening documentation...
    start README.md
    goto start
) else if "%choice%"=="8" (
    echo.
    echo Running quick test...
    quick_launch.bat
    goto start
) else (
    echo.
    echo Starting main launcher...
    python enhanced_launcher.py
)

echo.
echo ✅ Done.
pause >nul
