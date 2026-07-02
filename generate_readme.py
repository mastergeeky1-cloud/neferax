#!/usr/bin/env python3
"""
Regenerate README.md from hackingtool's internal tool metadata.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.theme import Theme
from core import HackingToolsCollection
from hackingtool import AllTools

_theme = Theme({"purple": "#FF4444"})
console = Console(theme=_theme)

TOOLS_PER_ROW = 4

HEADER = """\
<div align="center">

<img src="images/logo.svg" alt="Nefereax DarkAx" width="600">

<p><b>All-in-One Hacking Tool for Security Researchers & Pentesters</b></p>

[![License](https://img.shields.io/github/license/Nefereax/hackingtool)](LICENSE)&nbsp;
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)&nbsp;
[![Version](https://img.shields.io/badge/v2.0.0-FF4444?style=flat-square)](#)&nbsp;
[![Stars](https://img.shields.io/github/stars/Nefereax/hackingtool?style=flat-square&color=red)](https://github.com/Nefereax/hackingtool/stargazers)&nbsp;
[![Forks](https://img.shields.io/github/forks/Nefereax/hackingtool?style=flat-square&color=red)](https://github.com/Nefereax/hackingtool/network/members)&nbsp;
[![Issues](https://img.shields.io/github/issues/Nefereax/hackingtool?style=flat-square&color=red)](https://github.com/Nefereax/hackingtool/issues)&nbsp;
[![Last Commit](https://img.shields.io/github/last-commit/Nefereax/hackingtool?style=flat-square&color=FF4444)](https://github.com/Nefereax/hackingtool/commits/master)

![](https://img.shields.io/badge/20_Categories-7B61FF?style=for-the-badge)
![](https://img.shields.io/badge/185+_Tools-FF4444?style=for-the-badge)
![](https://img.shields.io/badge/19_Tags-FF61DC?style=for-the-badge)
![](https://img.shields.io/badge/Linux_%7C_Kali_%7C_Parrot_%7C_macOS-FFA116?style=for-the-badge&logo=linux&logoColor=white)

<a href="#installation"><img src="https://img.shields.io/badge/Install_Now-FF4444?style=for-the-badge&logo=rocket&logoColor=black" alt="Install Now"></a>&nbsp;
<a href="#quick-commands"><img src="https://img.shields.io/badge/Quick_Commands-7B61FF?style=for-the-badge&logo=terminal&logoColor=white" alt="Quick Commands"></a>&nbsp;
<a href="https://github.com/Nefereax/hackingtool/issues/new?template=tool_request.md"><img src="https://img.shields.io/badge/Suggest_a_Tool-FF61DC?style=for-the-badge&logo=plus&logoColor=white" alt="Suggest a Tool"></a>

</div>

---

## What's New in v2.0.0

<table>
<tr><td>

| | Feature | Description |
|:---:|---|---|
| **🐍** | **Python 3.10+** | All Python 2 code removed, modern syntax throughout |
| **🖥** | **OS-aware menus** | Linux-only tools hidden automatically on macOS |
| **📦** | **185+ tools** | 35 new modern tools added across 6 categories |
| **🔍** | **Search** | Type `/` to search all tools by name, description, or keyword |
| **🏷** | **Tag filter** | Type `t` to filter by 19 tags — osint, web, c2, cloud, mobile... |
| **🎯** | **Recommend** | Type `r` to get tool suggestions for a task description |
| **🖤** | **DarkAx Theme** | New dark red visual style with aggressive color scheme |
| **🏷** | **Nefereax Brand** | Full rebrand with Nefereax identity |

</td></tr>
</table>

---

## Installation
"""

QUICK_CMDS = """\

## Quick Commands

| Action | Command |
|---|---|
| Install | `curl -sSL https://raw.githubusercontent.com/Nefereax/hackingtool/master/install.sh | sudo bash` |
| Run | `hackingtool` |
| Update | `hackingtool` → `Update / Uninstall` → `Update Nefereax` |
| Uninstall | `hackingtool` → `Update / Uninstall` → `Uninstall Nefereax` |

---

## Tool Categories
"""


def generate_table(cat: HackingToolsCollection) -> str:
    rows = []
    tools = cat.TOOLS
    for i in range(0, len(tools), TOOLS_PER_ROW):
        row = tools[i:i + TOOLS_PER_ROW]
        cells = []
        for t in row:
            name = t.TITLE
            desc = (t.DESCRIPTION[:40] + "...") if len(t.DESCRIPTION) > 40 else t.DESCRIPTION
            cells.append(f"**{name}**<br><sub>{desc}</sub>")
        while len(cells) < TOOLS_PER_ROW:
            cells.append("")
        rows.append(" | ".join(cells))
    header = " | ".join(["---"] * TOOLS_PER_ROW)
    return "\n".join([f"| {' | '.join(cells)} |" for cells in
                      [row.split(" | ") for row in rows]])


def main():
    lines = [HEADER, QUICK_CMDS]

    for cat in AllTools().TOOLS:
        if isinstance(cat, HackingToolsCollection) and cat.TITLE != "All tools":
            lines.append(f"\n### {cat.TITLE}\n")
            lines.append(generate_table(cat))

    lines.append("""
---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Nefereax/hackingtool&type=Date)](https://star-history.com/#Nefereax/hackingtool&Date)

---

<p align="center">
  <i>Built with ❤️ by Nefereax — DarkAx Edition</i>
</p>
""")

    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
    with open(readme_path, "w") as f:
        f.writelines(lines)

    console.print("[bold green]README.md regenerated.[/bold green]")


if __name__ == "__main__":
    main()
