#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# Neferax DarkAx — Updater
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

INSTALL_DIR="/usr/share/neferax"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "[ERROR] Install directory not found: $INSTALL_DIR"
    echo "Reinstall with: curl -sSL https://raw.githubusercontent.com/Neferax/neferax/master/install.sh | sudo bash"
    exit 1
fi

cd "$INSTALL_DIR"
echo "[*] Pulling latest Neferax DarkAx code..."
git pull --rebase
echo "[✔] Neferax DarkAx updated."

if [ -f "requirements.txt" ] && [ -d "venv" ]; then
    echo "[*] Updating Python dependencies..."
    venv/bin/pip install --quiet -r requirements.txt
    echo "[✔] Dependencies updated."
fi

echo ""
echo "Done. Type neferax to start."
