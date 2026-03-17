@echo off
echo [loudio] Installing Python package...
pip install -e .
if %errorlevel% neq 0 (
    echo [loudio] Install failed. Make sure Python and pip are in PATH.
    exit /b 1
)
echo [loudio] Done! Run: loudio --help
