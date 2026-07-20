@echo off
title Mess Member Management System
cd /d "%~dp0"
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application closed with exit code %ERRORLEVEL%.
    pause
)
