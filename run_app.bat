@echo off
title Mess Member Management System
echo ===================================================
echo    Launching Mess Member Management System...
echo ===================================================
echo.

:: Ensure working directory is the project directory
cd /d "%~dp0"

:: Execute Python application
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application closed with exit code %ERRORLEVEL%.
    pause
)
