<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-e94560?style=for-the-badge&logo=github&logoColor=white"/>
  <img src="https://img.shields.io/badge/tools-114-58a6ff?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/chains-14-3fb950?style=for-the-badge&logo=kalilinux&logoColor=white"/>
  <img src="https://img.shields.io/badge/license-MIT-f0883e?style=for-the-badge"/>
</p>

<br>

```ascii
  ███╗   ██╗███████╗███████╗███████╗██████╗  █████╗ ██╗  ██╗
  ████╗  ██║██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗╚██╗██╔╝
  ██╔██╗ ██║█████╗  █████╗  █████╗  ██████╔╝███████║ ╚███╔╝
  ██║╚██╗██║██╔══╝  ██╔══╝  ██╔══╝  ██╔══██╗██╔══██║ ██╔██╗
  ██║ ╚████║███████╗██║     ███████╗██║  ██║██║  ██║██╔╝ ██╗
  ╚═╝  ╚═══╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
```

<p align="center">
  <strong>Dark Security Framework — 148 Precision Tools · 19 Attack Chains · HTML Reporting</strong>
  <br>
  <sub>Master the dark arts of penetration testing with elegance and precision.</sub>
</p>

<br>

---

## ⚡ Quick Start

```bash
# Install
sudo git clone https://github.com/mastergeeky1-cloud/neferax.git /usr/share/neferax
cd /usr/share/neferax && sudo python3 install.py

# Or run directly
sudo neferax scan 10.10.10.1          # Quick vulnerability scan
sudo neferax full target.com           # Full attack chain (19 suites)
sudo neferax list                       # Browse all 148 tools
sudo neferax search --method sqli       # Find SQL injection tools
sudo neferax reports                    # Open HTML report index
sudo neferax menu                       # Launch TUI
```

---

##  Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    neferax CLI                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────────┐  │
│  │  RECON  │  │   WEB   │  │ EXPLOIT │  │  PASSWORD  │  │
│  │ 27tools │  │ 13tools │  │ 6tools  │  │  8tools    │  │
│  └─────────┘  └─────────┘  └─────────┘  └───────────┘  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────────┐  │
│  │WIRELESS │  │ AD/WIN  │  │  CLOUD  │  │ CONTAINER  │  │
│  │ 11tools │  │ 7tools  │  │ 6tools  │  │  6tools    │  │
│  └─────────┘  └─────────┘  └─────────┘  └───────────┘  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────────┐  │
│  │ MOBILE  │  │ TUNNEL  │  │  MITM   │  │  TRAFFIC   │  │
│  │ 5tools  │  │ 5tools  │  │ 5tools  │  │  3tools    │  │
│  └─────────┘  └─────────┘  └─────────┘  └───────────┘  │
│  ┌─────────┐  ┌─────────┐                               │
│  │ REVERSE │  │  MISC   │                               │
│  │ 6tools  │  │ 4tools  │  19 ATTACK CHAINS              │
│  └─────────┘  └─────────┘                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────────┐  │
│  │ BINARY  │  │   PE    │  │ MEMORY  │  │ SCANNING   │  │
│  │ 11tools │  │ 7tools  │  │ 7tools  │  │  5tools    │  │
│  └─────────┘  └─────────┘  └─────────┘  └───────────┘  │
│  ┌─────────┐                                            │
│  │ATTACKING│   + HTML REPORTS                            │
│  │ 5tools  │                                            │
│  └─────────┘  └─────────┘                               │
└─────────────────────────────────────────────────────────┘
```

---

##   Attack Chains

| Chain | Description | Tools |
|---|---|---|
| `scan` | Quick vulnerability scan | nmap, naabu, gobuster, nikto |
| `recon` | Full reconnaissance | 9 tools across DNS, OSINT, port scan |
| `web` | Web app attack | whatweb, nikto, wpscan, gospider, dirb, gobuster, ffuf, sqlmap, nuclei |
| `exploit` | Exploitation | searchsploit, nmap, nuclei, hydra |
| `brute` | Brute force | hydra across ssh/ftp/http/mysql/smb |
| `osint` | OSINT gathering | theharvester, subfinder, dnsrecon, amass, cewl, httpx |
| `ad` | Active Directory | enum4linux, netexec, smbmap, responder, bloodhound, certipy, kerbrute |
| `wireless` | Wireless attacks | airmon, airodump, aireplay, aircrack, wifite, reaver, kismet |
| `password` | Password cracking | hashid, hashcat, john, crunch, cewl, pipal |
| `sql` | SQL injection | sqlmap, nuclei |
| `cloud` | Cloud security audit | s3scanner, prowler, scoutsuite, tfsec, checkov, cloudsploit |
| `container` | Container security | trivy, kubectl, kubescape, kube-hunter, dockle, hadolint |
| `mobile` | Mobile app security | apktool, dex2jar, jadx, objection, mobsf |
| `full` | Complete audit | All 13 chains above |

---

##   HTML Reporting

Every tool run generates a timestamped HTML report with dark theme:

```
~/.neferax/reports/
├── index.html              ← Report index (neferax reports)
├── 20260702_235959_nmap.html
├── 20260702_235959_gobuster.html
├── 20260702_235959_nikto.html
└── chain_20260702_235959_scan.html   ← Aggregated chain report
```

**Chain reports** include:
- Summary dashboard (pass/fail/timeout grid)
- Per-tool detailed reports with links
- Execution timeline
- Command and output for every tool

---

##   Permission Model

```bash
# Always run with sudo for full capability
sudo neferax scan 10.10.10.1

# Safe commands (no root needed)
neferax list              # Browse tools
neferax search nmap       # Search tools
neferax info hydra        # Tool details
neferax reports           # View reports
```

- 33 tools flagged as `SUDO_REQUIRED` (wireless, mitm, traffic, etc.)
- Running without root shows a clear warning
- `sudo neferax` → all tools work without per-command sudo

---

##   Attack Methods

Every tool is tagged with attack methods for powerful filtering:

```bash
# Find all SQL injection tools
neferax search --method sqli

# Find port scanners
neferax search --method port_scan

# Find OSINT tools
neferax search --method osint
```

---

##   All 148 Tools by Category

<details>
<summary><strong>RECON</strong> (27 tools)</summary>
<br>
nmap · masscan · netdiscover · arp-scan · theharvester · dnsrecon · dnsenum · fierce · amass · dmitry · enum4linux · netexec · smbmap · nbtscan · onesixtyone · snmpcheck · hping3 · fping · ike-scan · dnschef · recon-ng · spiderfoot · whois · onesixtyone · snmpcheck · httpx · subfinder · naabu
</details>

<details>
<summary><strong>WEB</strong> (13 tools)</summary>
<br>
nikto · whatweb · wpscan · skipfish · wafw00f · gobuster · dirb · ffuf · wfuzz · sqlmap · commix · lbd · gospider
</details>

<details>
<summary><strong>EXPLOIT</strong> (6 tools)</summary>
<br>
searchsploit · metasploit · hydra · ncrack · medusa · weevely
</details>

<details>
<summary><strong>PASSWORD</strong> (8 tools)</summary>
<br>
hashcat · john · crunch · cewl · hashid · gpp-decrypt · rsmangler · pipal
</details>

<details>
<summary><strong>WIRELESS</strong> (11 tools)</summary>
<br>
aircrack-ng · airodump-ng · aireplay-ng · airmon-ng · wifite · reaver · macchanger · kismet · mdk4 · bettercap · bully · pixiewps
</details>

<details>
<summary><strong>AD/WIN</strong> (7 tools)</summary>
<br>
responder · evil-winrm · samdump2 · chntpw · bloodhound · certipy · kerbrute
</details>

<details>
<summary><strong>CLOUD</strong> (6 tools)</summary>
<br>
s3scanner · prowler · scoutsuite · tfsec · checkov · cloudsploit
</details>

<details>
<summary><strong>CONTAINER</strong> (6 tools)</summary>
<br>
trivy · kubectl · kubescape · kube-hunter · dockle · hadolint
</details>

<details>
<summary><strong>MOBILE</strong> (5 tools)</summary>
<br>
apktool · dex2jar · jadx · objection · mobsf
</details>

<details>
<summary><strong>TUNNEL</strong> (5 tools)</summary>
<br>
proxychains · socat · ncat · iodine · redsocks
</details>

<details>
<summary><strong>MITM</strong> (5 tools)</summary>
<br>
mitmproxy · ettercap · sslstrip · sslscan · sslyze
</details>

<details>
<summary><strong>TRAFFIC</strong> (3 tools)</summary>
<br>
tcpdump · tshark · ngrep
</details>

<details>
<summary><strong>REVERSE</strong> (6 tools)</summary>
<br>
radare2 · gdb · nasm · binwalk · foremost · exiv2
</details>

<details>
<summary><strong>BINARY ANALYSIS</strong> (11 tools)</summary>
<br>
strings · xxd · objdump · readelf · strace · ltrace · nm · strip · objcopy · ropper · pwntools
</details>

<details>
<summary><strong>PE / .EXE</strong> (7 tools)</summary>
<br>
pecheck · pe-sieve · floss · capa · peframe · detect-it-easy
</details>

<details>
<summary><strong>MEMORY FORENSICS</strong> (7 tools)</summary>
<br>
volatility · volatility3 · avml · lime · scanmem · memdump · gcore
</details>

<details>
<summary><strong>SCANNING</strong> (5 tools)</summary>
<br>
rustscan · zmap · zgrab · crackmapexec · impacket
</details>

<details>
<summary><strong>ATTACKING</strong> (5 tools)</summary>
<br>
mimikatz · msfvenom · chisel · ligolo-ng · beef
</details>

<details>
<summary><strong>MISC</strong> (4 tools)</summary>
<br>
arping · windows-binaries · webshells · laudanum
</details>

---

##   TUI — Terminal User Interface

Launch the interactive menu:

```bash
sudo neferax menu
# or
neferax
```

Features:
- Rich-styled panels with color-coded categories
- Real-time tool execution with streaming output
- Installed/not-installed detection per tool
- Keyboard-navigable menus

---

##   Installation

### From GitHub (recommended)
```bash
git clone https://github.com/mastergeeky1-cloud/neferax.git /usr/share/neferax
cd /usr/share/neferax
sudo python3 install.py

# Launchers installed:
/usr/bin/neferax      # CLI
/usr/bin/neferax-tui   # TUI
```

### Manual
```bash
sudo ln -s /usr/share/neferax/neferax_cli.py /usr/bin/neferax
sudo ln -s /usr/share/neferax/neferax_cli.py /usr/bin/neferax
sudo ln -s /usr/share/neferax/neferax_tui.py /usr/bin/neferax-tui
```

---

##   CI/CD

| Workflow | Status |
|---|---|
| Test Install | ✅ Automated install + smoke test on push |
| Python Lint | ✅ ruff checking (E9, F63, F7, F82, PLE, YTT) |

---

##   Roadmap

- [x] 148 tools across 14 categories
- [x] 19 attack chains with aggregated HTML reports
- [x] Permission-aware execution (auto-sudo)
- [x] Attack method tagging and filtering
- [ ] Parallel multi-target execution
- [ ] Plugin system for community tools
- [ ] REST API + Web dashboard
- [ ] Database-backed findings storage
- [ ] Distributed agent mode

---

<p align="center">
  <strong>NEFERAX</strong> — <em>Dark Security Framework</em>
  <br>
  <sub>mastergeeky1-cloud/neferax</sub>
</p>
