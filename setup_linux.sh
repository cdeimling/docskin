#!/bin/bash
set -e

echo "\n========== Docskin Environment Setup =========="
echo "[2/5] Checking for 'uv' package manager..."
if ! command -v uv &> /dev/null; then
	echo "'uv' not found. Installing via official script..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
else
	echo "'uv' is already installed."
fi


echo "[3/3] Installing all Python dependencies from pyproject.toml using uv..."
uv sync --locked

uv run docskin setup

