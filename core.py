import os
import shutil
import sys
import webbrowser
from collections.abc import Callable
from platform import system

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich.traceback import install

from constants import (
    THEME_PRIMARY, THEME_BORDER, THEME_ACCENT,
    THEME_SUCCESS, THEME_ERROR, THEME_WARNING,
    THEME_DIM, THEME_ARCHIVED, THEME_URL,
)

# Enable rich tracebacks globally
install()

_theme = Theme({
    "purple":   "#7B61FF",
    "success":  THEME_SUCCESS,
    "error":    THEME_ERROR,
    "warning":  THEME_WARNING,
    "archived": THEME_ARCHIVED,
    "url":      THEME_URL,
    "dim":      THEME_DIM,
})

# Single shared console — all tool files do: from core import console
console = Console(theme=_theme)


def clear_screen():
    os.system("cls" if system() == "Windows" else "clear")


def validate_input(ip, val_range: list) -> int | None:
    """Return the integer if it is in val_range, else None."""
    if not val_range:
        return None
    try:
        ip = int(ip)
        if ip in val_range:
            return ip
    except (TypeError, ValueError):
        pass
    return None


def _show_inline_help():
    """Quick help available from any menu level."""
    console.print(Panel(
        Text.assemble(
            ("  Navigation\n", "bold white"),
            ("  ─────────────────────────────────\n", "dim"),
            ("  1–N    ", "bold cyan"), ("select item\n", "white"),
            ("  97     ", "bold cyan"), ("install all (in category)\n", "white"),
            ("\n  Tool menu: Install, Run, Update, Open Folder\n", "dim"),
            ("  99     ", "bold cyan"), ("go back\n", "white"),
            ("  98     ", "bold cyan"), ("open project page / archived\n", "white"),
            ("  ?      ", "bold cyan"), ("show this help\n", "white"),
            ("  q      ", "bold cyan"), ("quit Nefereax\n", "white"),
        ),
        title="[bold bright_red] ? Quick Help [/bold bright_red]",
        border_style="bright_red",
        box=box.ROUNDED,
        padding=(0, 2),
    ))
    Prompt.ask("[dim]Press Enter to return[/dim]", default="")


class HackingTool:
    TITLE: str              = ""
    DESCRIPTION: str        = ""
    INSTALL_COMMANDS: list  = []
    RUN_COMMANDS: list      = []
    PROJECT_URL: str        = ""
    TAGS: list[str]         = []
    ARCHIVED: bool          = False
    SUPPORTED_OS: list      = []

    def __init__(self, options: list | None = None,
                 installable: bool = True,
                 runnable: bool = True):
        self.installable = installable
        self.runnable    = runnable
        self._options    = options or []

    @property
    def full_title(self) -> str:
        archived = " [dim yellow](archived)[/dim yellow]" if self.ARCHIVED else ""
        return f"{self.TITLE}{archived}"

    def show_options(self):
        clear_screen()
        desc = self.DESCRIPTION
        tags = ""
        if self.TAGS:
            tags = f" [dim]| Tags: {', '.join(self.TAGS)}[/dim]"
        console.print(Panel(
            Text(desc + ("\n\n" + "─" * 60 if self._options else "") + tags, style="white"),
            title=f"[bold red] {self.full_title} [/bold red]",
            border_style="bright_red",
        ))
        while True:
            if self._options:
                table = Table(border_style="red", box=box.ROUNDED, show_header=False)
                table.add_column("#", style="bold red", width=4, justify="right")
                table.add_column("Option", style="white")
                for i, (name, _) in enumerate(self._options, 1):
                    table.add_row(str(i), name)
                console.print(table)

            choices = []
            if self.installable:
                choices.append("[bold red]1[/bold red] Install")
            if self.runnable:
                choices.append("[bold red]2[/bold red] Run")
            choices.append("[bold red]99[/bold red] Back")
            console.print("  " + "  |  ".join(choices))

            choice = Prompt.ask("  [bold red]> ")

            if choice == "99":
                return
            if self._options:
                try:
                    idx = int(choice)
                    if 1 <= idx <= len(self._options):
                        self._options[idx - 1][1]()
                        continue
                except ValueError:
                    pass
            if choice == "1" and self.installable:
                self.install()
            elif choice == "2" and self.runnable:
                self.run()
            else:
                _show_inline_help()

    def install(self):
        priv = ""
        if os.geteuid() != 0:
            from constants import PRIV_CMD
            priv = f"{PRIV_CMD} "
        env = os.environ.copy()
        if self.INSTALL_COMMANDS:
            for cmd in self.INSTALL_COMMANDS:
                console.print(f"[bold cyan]> {cmd}[/bold cyan]")
                rc = subprocess.call(f"{priv}{cmd}", shell=True, env=env)
                if rc != 0:
                    console.print(f"[error]Command failed (rc={rc})[/error]")
                    break
            else:
                console.print("[success]✔ Done[/success]")
        else:
            console.print("[yellow]No install instructions for this tool.[/yellow]")
        Prompt.ask("[dim]Press Enter[/dim]", default="")

    def run(self):
        if self.RUN_COMMANDS:
            for cmd in self.RUN_COMMANDS:
                console.print(f"[bold cyan]> {cmd}[/bold cyan]")
                rc = subprocess.call(cmd, shell=True)
                if rc != 0:
                    console.print(f"[warning]Command exited with rc={rc}[/warning]")
        else:
            console.print("[yellow]No run command defined.[/yellow]")
        Prompt.ask("[dim]Press Enter[/dim]", default="")

    def update(self):
        console.print("[yellow]No update logic defined for this tool.[/yellow]")


class HackingToolsCollection:
    TITLE: str = ""
    DESCRIPTION: str = ""
    TOOLS: list[HackingTool] = []

    def __init__(self):
        self._archived: list[HackingTool] = []
        self._incompatible: list[HackingTool] = []

    def show_options(self):
        clear_screen()
        console.print(Panel(
            Text(f"[bold red]{self.TITLE}[/bold red]"),
            border_style="bright_red",
        ))

        active = [t for t in self.TOOLS if not t.ARCHIVED]
        archived = [t for t in self.TOOLS if t.ARCHIVED]

        table = Table(border_style="red", box=box.ROUNDED)
        table.add_column("#", style="bold red", width=4, justify="right")
        table.add_column("Tool", style="bold red")
        table.add_column("Description", style="dim white", no_wrap=False)
        table.add_column("Tags", style="dim yellow", width=20)

        for i, t in enumerate(active, 1):
            tags_short = ", ".join(t.TAGS[:3]) if t.TAGS else ""
            desc = (t.DESCRIPTION[:55] + "...") if len(t.DESCRIPTION) > 55 else t.DESCRIPTION
            table.add_row(str(i), t.TITLE, desc, tags_short)

        if archived:
            table.add_section()
            for i, t in enumerate(archived, len(active) + 1):
                tags_short = ", ".join(t.TAGS[:3]) if t.TAGS else ""
                desc = (t.DESCRIPTION[:55] + "...") if len(t.DESCRIPTION) > 55 else t.DESCRIPTION
                table.add_row(str(i), f"[dim yellow]{t.TITLE}[/dim yellow]",
                              f"[dim yellow]{desc}[/dim yellow]",
                              f"[dim yellow]{tags_short}[/dim yellow]")

        if self.DESCRIPTION:
            console.print(Panel(Text(self.DESCRIPTION, style="italic dim"), border_style="dim"))
        console.print(table)
        console.print("  [dim]97 Install All  |  98 Project Page  |  99 Back[/dim]")

        while True:
            choice = Prompt.ask("  [bold red]> ")

            if choice == "99":
                return
            if choice == "98":
                self._open_project_page()
                continue
            if choice == "97":
                self._install_all()
                continue
            try:
                idx = int(choice)
                if 1 <= idx <= len(self.TOOLS):
                    self.TOOLS[idx - 1].show_options()
            except ValueError:
                pass

    def _install_all(self):
        priv = ""
        if os.geteuid() != 0:
            from constants import PRIV_CMD
            priv = f"{PRIV_CMD} "
        for t in self.TOOLS:
            if t.INSTALL_COMMANDS:
                for cmd in t.INSTALL_COMMANDS:
                    console.print(f"[bold cyan]> {cmd}[/bold cyan]")
                    rc = subprocess.call(f"{priv}{cmd}", shell=True)
                    if rc != 0:
                        console.print(f"[error]Failed: {cmd}[/error]")
        console.print("[success]✔ All installed[/success]")
        Prompt.ask("[dim]Press Enter[/dim]", default="")

    def _open_project_page(self):
        proj_urls = [t.PROJECT_URL for t in self.TOOLS if t.PROJECT_URL]
        if proj_urls:
            webbrowser.open(proj_urls[0])
        else:
            console.print("[yellow]No project URL available.[/yellow]")
