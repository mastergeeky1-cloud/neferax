from pathlib import Path
import platform
import shutil as _shutil

REPO_OWNER   = "mastergeeky1-cloud"
REPO_NAME    = "hackingtool"
GITHUB_REPO  = "neferax"
REPO_URL     = f"https://github.com/{REPO_OWNER}/{GITHUB_REPO}.git"
REPO_WEB_URL = f"https://github.com/{REPO_OWNER}/{GITHUB_REPO}"

VERSION         = "2.0.0"
VERSION_DISPLAY = f"v{VERSION}"
MIN_PYTHON = (3, 10)

USER_CONFIG_DIR  = Path.home() / f".{REPO_NAME}"
USER_TOOLS_DIR   = USER_CONFIG_DIR / "tools"
USER_CONFIG_FILE = USER_CONFIG_DIR / "config.json"
USER_LOG_FILE    = USER_CONFIG_DIR / f"{REPO_NAME}.log"

_system = platform.system()
if _system == "Darwin":
    APP_INSTALL_DIR = Path("/usr/local/share") / REPO_NAME
    APP_BIN_PATH    = Path("/usr/local/bin")   / REPO_NAME
elif _system == "Linux":
    APP_INSTALL_DIR = Path("/usr/share") / REPO_NAME
    APP_BIN_PATH    = Path("/usr/bin")   / REPO_NAME
else:
    APP_INSTALL_DIR = USER_CONFIG_DIR / "app"
    APP_BIN_PATH    = USER_CONFIG_DIR / "bin" / REPO_NAME

THEME_PRIMARY  = "bold bright_red"
THEME_BORDER   = "bold red"
THEME_SUCCESS  = "bold green"
THEME_ERROR    = "bold red"
THEME_WARNING  = "bold yellow"
THEME_DIM      = "dim white"
THEME_ARCHIVED = "dim yellow"
THEME_URL      = "underline bright_blue"
THEME_ACCENT   = "bold cyan"

DEFAULT_CONFIG: dict = {
    "tools_dir":      str(USER_TOOLS_DIR),
    "version":        VERSION,
    "theme":          "darkax",
    "show_archived":  False,
    "sudo_binary":    "sudo",
    "go_bin_dir":     str(Path.home() / "go" / "bin"),
    "gem_bin_dir":    str(Path.home() / ".gem" / "ruby"),
}

PRIV_CMD = "doas" if _shutil.which("doas") else "sudo"
