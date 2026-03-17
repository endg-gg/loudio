#!/usr/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing loudio..."

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not installed"
    exit 1
fi

if ! python3 -m venv --help &> /dev/null; then
    echo "Error: python3-venv is missing. Install it first."
    exit 1
fi

# Install system deps
echo "Installing system dependencies..."
if command -v apt &> /dev/null; then
    sudo apt install -y libopus-dev portaudio19-dev
elif command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm opus portaudio
elif command -v dnf &> /dev/null; then
    sudo dnf install -y opus-devel portaudio-devel
else
    echo "Warning: Unsupported package manager. Install libopus and portaudio manually."
fi

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip -q

echo "Installing dependencies..."
pip install -r requirements.txt -q

INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

cat > "$INSTALL_DIR/loudio" << EOF
#!/usr/bin/bash
source "$SCRIPT_DIR/.venv/bin/activate"
exec python3 "$SCRIPT_DIR/main.py" "\$@"
EOF

chmod +x "$INSTALL_DIR/loudio"

SHELL_NAME=$(basename "$SHELL")
if [ "$SHELL_NAME" = "zsh" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
else
    SHELL_CONFIG="$HOME/.bashrc"
fi

if ! grep -q '.local/bin' "$SHELL_CONFIG" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
    echo "Added $HOME/.local/bin to PATH in $SHELL_CONFIG"
    echo "Run: source $SHELL_CONFIG"
fi

echo ""
echo "loudio installed successfully!"
echo "Run with: loudio --help"
