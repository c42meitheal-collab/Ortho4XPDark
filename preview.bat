@echo off
echo.
echo ORTHO4XPDARK PREVIEW
echo ====================
echo.
echo Question: Does our preview reflect the current visual end state?
echo.
echo HONEST ANSWER: 
echo The previous preview was too optimistic about what works.
echo Let me show you what actually works vs what needs setup.
echo.
echo WHAT THIS PREVIEW SHOWS:
echo - What works immediately (dark theme, basic tools)
echo - What needs dependencies (XRoads, advanced features) 
echo - How to fix missing functionality
echo.
echo This is just a hobbyist dark theme mod.
echo.
echo [1] Dark Theme Demo (Should work)
echo [2] XRoads Test (Might fail - needs dependencies)
echo [3] Install Dependencies (Fix the failing stuff)
echo [4] Read Documentation
echo [5] System Check
echo.
set /p choice="Pick option (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting dark theme demo...
    python Ortho4XPDark.py
    if %ERRORLEVEL% neq 0 (
        echo Failed to start dark theme. Check if Python is installed.
    )
) else if "%choice%"=="2" (
    echo.
    echo Testing XRoads might fail if dependencies missing...
    python test_xroads.py
    if %ERRORLEVEL% neq 0 (
        echo XRoads test failed. Try option 3 to install dependencies.
    )
) else if "%choice%"=="3" (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
    if %ERRORLEVEL% equ 0 (
        echo Dependencies installed! XRoads should work now.
    ) else (
        echo Install failed. Check GDAL_INSTALLATION.md for help.
    )
) else if "%choice%"=="4" (
    echo.
    echo Opening documentation...
    if exist README.md (
        start README.md
    ) else (
        echo README.md not found
    )
) else if "%choice%"=="5" (
    echo.
    echo Running system check...
    python system_verification.py
    if %ERRORLEVEL% neq 0 (
        echo System check failed. Check Python installation.
    )
) else (
    echo.
    echo Invalid choice. Starting dark theme...
    python Ortho4XPDark.py
)

echo.
echo BOTTOM LINE:
echo Previous preview was aspirational - showed what I wanted to work.
echo This preview is realistic - shows what actually works.
echo Install dependencies to bridge the gap.
echo.
echo This is a hobbyist modification to make Ortho4XP dark-themed.
echo.
pause
