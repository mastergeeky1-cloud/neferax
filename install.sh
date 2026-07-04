#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# Neferax DarkAx — One-liner installer
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/Neferax/neferax/master/install.sh | sudo bash
#
# What it does:
#   1. Checks prerequisites (Python 3.10+, git, pip, venv)
#   2. Clones the repository to /usr/share/neferax
#   3. Creates a Python venv and installs requirements
#   4. Creates a launcher at /usr/bin/neferax
#   5. Creates user directories at ~/.neferax/
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

REPO_URL="https://github.com/Neferax/neferax.git"
INSTALL_DIR="/usr/share/neferax"
BIN_PATH="/usr/bin/neferax"
CONFIG_DIR="${SUDO_USER:+$(eval echo ~"$SUDO_USER")}/.neferax"
: "${CONFIG_DIR:=$HOME/.neferax}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()  { echo -e "${CYAN}[*]${RESET} $1"; }
ok()    { echo -e "${GREEN}[✔]${RESET} $1"; }
warn()  { echo -e "${YELLOW}[!]${RESET} $1"; }
fail()  { echo -e "${RED}[✘]${RESET} $1"; exit 1; }

if [ "$(id -u)" -ne 0 ]; then
    fail "This installer must be run as root.\n    Usage: curl -sSL <url> | ${BOLD}sudo${RESET} bash"
fi

echo ""
echo -e "${BOLD}${RED}  ⚔  Neferax DarkAx Installer${RESET}"
echo -e "  ─────────────────────────────────────"
echo ""

if command -v apt-get &>/dev/null; then
    PKG_MGR="apt-get"
    PKG_UPDATE="apt-get update -qq"
    PKG_INSTALL="apt-get install -y -qq"
elif command -v pacman &>/dev/null; then
    PKG_MGR="pacman"
    PKG_UPDATE="pacman -Sy --noconfirm"
    PKG_INSTALL="pacman -S --noconfirm --needed"
elif command -v dnf &>/dev/null; then
    PKG_MGR="dnf"
    PKG_UPDATE="true"
    PKG_INSTALL="dnf install -y -q"
elif command -v brew &>/dev/null; then
    PKG_MGR="brew"
    PKG_UPDATE="true"
    PKG_INSTALL="brew install"
else
    fail "No supported package manager found (need apt-get, pacman, dnf, or brew)."
fi
info "Package manager: ${BOLD}$PKG_MGR${RESET}"

info "Installing prerequisites..."
$PKG_UPDATE 2>/dev/null || true

for pkg in git curl python3 python3-pip python3-venv; do
    if [ "$PKG_MGR" = "pacman" ]; then
        case "$pkg" in
            python3)     pkg="python" ;;
            python3-pip) pkg="python-pip" ;;
            python3-venv) continue ;;
        esac
    elif [ "$PKG_MGR" = "brew" ]; then
        case "$pkg" in
            python3-pip|python3-venv) continue ;;
        esac
    elif [ "$PKG_MGR" = "dnf" ]; then
        case "$pkg" in
            python3-venv) continue ;;
        esac
    fi
    $PKG_INSTALL "$pkg" 2>/dev/null || warn "Could not install $pkg — may already be present"
done

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]; }; then
    fail "Python 3.10+ required. Found: Python $PYTHON_VERSION"
fi
ok "Python $PYTHON_VERSION"

if [ -d "$INSTALL_DIR" ]; then
    warn "$INSTALL_DIR already exists."
    read -rp "    Replace it? [y/N] " answer
    if [[ "$answer" =~ ^[Yy] ]]; then
        rm -rf "$INSTALL_DIR"
    else
        fail "Installation aborted."
    fi
fi

info "Cloning repository..."
git clone --depth 1 "$REPO_URL" "$INSTALL_DIR" 2>/dev/null
ok "Cloned to $INSTALL_DIR"

info "Creating virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"

info "Installing Python dependencies..."
"$INSTALL_DIR/venv/bin/pip" install --quiet -r "$INSTALL_DIR/requirements.txt" 2>/dev/null
ok "Dependencies installed"

cat > "$BIN_PATH" << 'LAUNCHER'
#!/bin/bash
source "/usr/share/neferax/venv/bin/activate"
python3 "/usr/share/neferax/neferax.py" "$@"
LAUNCHER
chmod 755 "$BIN_PATH"
ok "Launcher installed at $BIN_PATH"

mkdir -p "$CONFIG_DIR/tools"
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    cat > "$CONFIG_DIR/config.json" << CONF
{
  "tools_dir": "$CONFIG_DIR/tools",
  "version": "2.0.0"
}
CONF
fi
if [ -n "${SUDO_USER:-}" ]; then
    chown -R "$SUDO_USER:$SUDO_USER" "$CONFIG_DIR"
fi
ok "User config: $CONFIG_DIR"

echo ""
echo -e "${GREEN}${BOLD}  ✔  Installation complete!${RESET}"
echo -e "  Type ${BOLD}${CYAN}neferax${RESET} to start."
echo ""
