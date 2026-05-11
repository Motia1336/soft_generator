@echo off
setlocal enabledelayedexpansion

echo =============================================
echo  Mobile Profile Manager - Build Script
echo =============================================

:: 1. Настройка базового Python
set PYTHON=python

:: 2. Очистка старого окружения, если оно битое
if exist ".venv" (
    echo [0/4] Cleaning old virtual environment...
    rmdir /S /Q ".venv"
)

:: 3. Создание нового виртуального окружения
echo [1/4] Creating fresh virtual environment...
%PYTHON% -m venv .venv
if errorlevel 1 (
    echo ERROR: Could not create virtual environment. Make sure Python is installed and in PATH.
    pause
    exit /b 1
)

:: 4. Установка путей внутри venv
set VENV_PYTHON="%~dp0.venv\Scripts\python.exe"
set VENV_PIP="%~dp0.venv\Scripts\pip.exe"

:: 5. Установка зависимостей
echo [2/4] Installing dependencies...
%VENV_PIP% install -U pip
%VENV_PIP% install -r requirements.txt
%VENV_PIP% install pyinstaller customtkinter pillow

:: 6. Очистка старых билдов
echo [3/4] Cleaning previous build artifacts...
if exist "build" rmdir /S /Q "build"
if exist "dist" rmdir /S /Q "dist"
if exist "ProfileManager.exe" del /Q "ProfileManager.exe"

:: 7. Сборка EXE
echo [4/4] Building executable (clean build)...
%VENV_PYTHON% -m PyInstaller --clean --noconfirm --onefile --windowed --name "ProfileManager" --icon=NONE --add-data "generator.py;." --add-data "device_database.py;." --hidden-import device_database --hidden-import customtkinter --hidden-import PIL --collect-all customtkinter main.py

:: 8. Финализация
if exist "dist\ProfileManager.exe" (
    copy /Y "dist\ProfileManager.exe" "ProfileManager.exe"
    echo.
    echo =============================================
    echo  DONE! ProfileManager.exe updated.
    echo =============================================
) else (
    echo.
    echo ERROR: Build failed, dist\ProfileManager.exe not found!
)

pause
