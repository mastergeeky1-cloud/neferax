#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from pathlib import Path

# ── Python version check (must be before any other local import) ──────────────
if sys.version_info < (3, 10):
    print(
        f"[ERROR] Python 3.10 or newer is required.\n"
        f"You are running Python {sys.version_info.major}.{sys.version_info.minor}.\n"
        f"Install with: sudo apt install python3.10"
    )
    sys.exit(1)

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich import box

from constants import (
    REPO_URL, APP_INSTALL_DIR, APP_BIN_PATH,
    VERSION, VERSION_DISPLAY,
    USER_CONFIG_DIR, USER_TOOLS_DIR, USER_CONFIG_FILE,
    DEFAULT_CONFIG,
)
from os_detect import CURRENT_OS, REQUIRED_PACKAGES, PACKAGE_UPDATE_CMDS, PACKAGE_INSTALL_CMDS

console = Console()

VENV_DIR_NAME = "venv"
REQUIREMENTS   = "requirements.txt"


# ── Privilege check ────────────────────────────────────────────────────────────

def check_root():
    if os.geteuid() != 0:
        console.print("[red]This installer must be run as root.[/red]")
        sys.exit(1)


# ── Prerequisites ──────────────────────────────────────────────────────────────

def install_prerequisites():
    os_name = CURRENT_OS.system
    mgr = CURRENT_OS.pkg_manager
    update_cmd = PACKAGE_UPDATE_CMDS.get(mgr)
    install_cmd = PACKAGE_INSTALL_CMDS.get(mgr)

    if update_cmd:
        console.print(f"[dim]Updating package lists ({mgr})...[/dim]")
        subprocess.run(update_cmd, shell=True, check=False)

    to_install = REQUIRED_PACKAGES.get(os_name, [])
    if not to_install:
        to_install = REQUIRED_PACKAGES.get("default", [])

    if to_install and install_cmd:
        full_cmd = f"{install_cmd} {' '.join(to_install)}"
        console.print(f"[dim]Installing prerequisites: {' '.join(to_install)}[/dim]")
        subprocess.run(full_cmd, shell=True, check=False)
    else:
        console.print("[yellow]No prerequisites to install or package manager unknown.[/yellow]")


# ── Clone / install ────────────────────────────────────────────────────────────

def clone_repo():
    if APP_INSTALL_DIR.exists():
        console.print(f"[green]✔ {APP_INSTALL_DIR} already present — skipping clone[/green]")
        return
    console.print(f"[dim]Cloning from {REPO_URL}...[/dim]")
    result = subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, str(APP_INSTALL_DIR)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        console.print(f"[red]Clone failed:\n{result.stderr}[/red]")
        sys.exit(1)
    console.print(f"[green]✔ Cloned to {APP_INSTALL_DIR}[/green]")


def create_venv():
    venv_path = APP_INSTALL_DIR / VENV_DIR_NAME
    console.print("[dim]Creating virtual environment...[/dim]")
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    pip_path = venv_path / "bin" / "pip"
    req_path = APP_INSTALL_DIR / REQUIREMENTS
    if req_path.exists():
        console.print("[dim]Installing Python dependencies...[/dim]")
        subprocess.run([str(pip_path), "install", "-q", "-r", str(req_path)], check=False)
    return venv_path


def create_launcher(venv_path):
    launcher_dir = Path("/usr/bin")
    for name, entry in [("hackingtool","hackingtool.py"),("nefereax","nefereax_cli.py"),("neferax","nefereax_cli.py")]:
        l = launcher_dir / name
        l.write_text('#!/bin/bash\n'
            'source "' + str(venv_path) + '/bin/activate"\n'
            'python3 "' + str(APP_INSTALL_DIR / entry) + '" "$@"\n')
        l.chmod(0o755)
        console.print(f"[green]✔ Launcher installed at {l}[/green]")


def setup_user_config():
    USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    (USER_CONFIG_DIR / "tools").mkdir(parents=True, exist_ok=True)
    if not USER_CONFIG_FILE.exists():
        DEFAULT_CONFIG["tools_dir"] = str(USER_TOOLS_DIR)
        import json
        USER_CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2))
    console.print(f"[green]✔ User config: {USER_CONFIG_DIR}[/green]")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    console.print()
    console.print(Panel(
        Text(f"Nefereax DarkAx Installer  {VERSION_DISPLAY}", style="bold red"),
        box=box.DOUBLE, border_style="bright_red",
    ))
    console.print()

    non_interactive = len(sys.argv) > 1 and sys.argv[1] == "1"

    check_root()
    install_prerequisites()
    clone_repo()
    venv_path = create_venv()
    create_launcher(venv_path)
    setup_user_config()

    console.print()
    console.print("[bold green]  ✔  Installation complete![/bold green]")
    console.print("  Type [bold cyan]hackingtool[/bold cyan] to start.")
    console.print()


if __name__ == "__main__":
    main()
