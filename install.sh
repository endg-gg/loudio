#!/usr/bin/env bash
set -e

echo "[loudio] Installing system dependencies..."

if command -v apt &>/dev/null; then
    sudo apt install -y libopus-dev portaudio19-dev
elif command -v pacman &>/dev/null; then
    sudo pacman -S --noconfirm opus portaudio
elif command -v dnf &>/dev/null; then
    sudo dnf install -y opus-devel portaudio-devel
else
    echo "Unsupported package manager. Install libopus and portaudio manually."
fi

echo "[loudio] Installing Python package..."
pip install -e .

echo "[loudio] Done! Run: loudio --help"
