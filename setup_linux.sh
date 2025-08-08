#!/bin/bash
set -e

echo "\n========== Docskin Environment Setup =========="

echo "[1/5] Installing system dependencies for WeasyPrint..."
sudo apt-get update -qq
sudo apt-get install -y libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libffi-dev

echo "[2/5] Checking for 'uv' package manager..."
if ! command -v uv &> /dev/null; then
	echo "'uv' not found. Installing via official script..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
else
	echo "'uv' is already installed."
fi


echo "[3/3] Installing all Python dependencies from pyproject.toml using uv..."
uv sync

echo "\n✅ Setup complete!"
echo "To activate your environment later, run: source .venv/bin/activate"

