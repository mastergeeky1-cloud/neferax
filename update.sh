#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# Nefereax DarkAx — Updater
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

INSTALL_DIR="/usr/share/hackingtool"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "[ERROR] Install directory not found: $INSTALL_DIR"
    echo "Reinstall with: curl -sSL https://raw.githubusercontent.com/Nefereax/hackingtool/master/install.sh | sudo bash"
    exit 1
fi

cd "$INSTALL_DIR"
echo "[*] Pulling latest Nefereax DarkAx code..."
git pull --rebase
echo "[✔] Nefereax DarkAx updated."

if [ -f "requirements.txt" ] && [ -d "venv" ]; then
    echo "[*] Updating Python dependencies..."
    venv/bin/pip install --quiet -r requirements.txt
    echo "[✔] Dependencies updated."
fi

echo ""
echo "Done. Type hackingtool to start."
