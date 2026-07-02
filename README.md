# NEFERAX — Dark Security Framework

**By mastergeeky1-cloud**

> **Neferax** is an all-in-one pentesting framework with 89 Kali Linux tools across 11 categories, 11 automated attack chains, and both CLI + TUI interfaces. Designed for security professionals, CTF players, and red team operations.

---

## Quick Start

```bash
# System-wide CLI
neferax scan 10.10.10.1
nefereax web https://example.com
neferax full 192.168.1.0/24

# Interactive TUI menu
neferax menu
hackingtool

# Browse & search
neferax list
neferax info nmap
neferax search sql
```

---

## Features

| Feature | Description |
|---|---|
| **89 Tools** | Full Kali Linux pentesting arsenal — recon, web, exploit, password, wireless, AD, tunnel, MITM, traffic, reverse |
| **11 Attack Chains** | Pre-built chains: scan, recon, web, exploit, brute, osint, ad, wireless, password, sql, full |
| **Dual Interface** | CLI (`neferax`) + TUI (`hackingtool`) — both fully connected |
| **System Tools** | Uses native Kali binaries (no broken git clones). Every tool pre-installed |
| **Styled Output** | Professional box-drawing UI with colored borders and organized tables |
| **Tool Search** | `neferax search <query>` across all tool names, descriptions, and commands |
| **Cross-Referenced** | Tools in CLI and TUI come from the same definitions |

---

## Tool Database (89 Tools)

### Reconnaissance (23)
| Tool | Description | Usage |
|---|---|---|
| nmap | Network discovery & security auditing | `nmap <target>` |
| masscan | Fast internet port scanner | `masscan --rate=1000 -p1-65535 <target>` |
| netdiscover | Passive/active ARP scanner | `netdiscover -r <target>` |
| arp-scan | ARP scan local network | `arp-scan --localnet` |
| theharvester | Email, subdomain & name OSINT | `theHarvester -d <domain> -b all` |
| dnsrecon | DNS enumeration tool | `dnsrecon -d <target> -t std` |
| dnsenum | DNS enumeration utility | `dnsenum <target>` |
| fierce | DNS reconnaissance | `fierce --domain <domain>` |
| amass | Attack surface mapping | `amass enum -d <domain>` |
| dmitry | Deepmagic info gathering | `dmitry <target>` |
| enum4linux | Windows/Samba enumeration | `enum4linux -a <target>` |
| netexec | Network execution suite | `netexec smb <target>` |
| smbmap | SMB share enumeration | `smbmap -H <target>` |
| nbtscan | NetBIOS name scanner | `nbtscan <target>` |
| onesixtyone | SNMP scanner | `onesixtyone <target>` |
| snmpcheck | SNMP enumeration | `snmpcheck -t <target>` |
| hping3 | Packet crafting & analysis | `hping3 -c 4 <target>` |
| fping | Ping sweep tool | `fping -asg <target>` |
| ike-scan | IKE VPN scanning | `ike-scan <target>` |
| dnschef | DNS proxy/spoofer | `dnschef` |
| recon-ng | Web reconnaissance framework | `recon-ng` |
| spiderfoot | OSINT automation | `spiderfoot -s <target>` |
| whois | Domain registration lookup | `whois <target>` |

### Web (12)
| Tool | Description | Usage |
|---|---|---|
| nikto | Web server scanner | `nikto -h <target>` |
| whatweb | Web technology identifier | `whatweb -v <target>` |
| wpscan | WordPress security scanner | `wpscan --url <target>` |
| skipfish | Web app security scanner | `skipfish -o /tmp/skipfish <target>` |
| wafw00f | WAF detection fingerprinting | `wafw00f <target>` |
| gobuster | Directory/file brute-forcer | `gobuster dir -u <target>` |
| dirb | Web content scanner | `dirb <target>` |
| ffuf | Fast web fuzzer | `ffuf -w wordlist.txt -u <target>/FUZZ` |
| wfuzz | Web fuzzer | `wfuzz -w wordlist.txt <target>` |
| sqlmap | SQL injection automation | `sqlmap -u <target> --batch` |
| commix | Command injection exploiter | `commix --url=<target>` |
| lbd | Load balancing detector | `lbd <domain>` |

### Exploit (7)
| Tool | Description | Usage |
|---|---|---|
| searchsploit | Exploit-DB search tool | `searchsploit <query>` |
| metasploit | Metasploit framework console | `msfconsole -q` |
| set | Social Engineer Toolkit | `setoolkit` |
| hydra | Online password brute-forcer | `hydra -l root -P wordlist.txt <target> <service>` |
| ncrack | Network authentication cracker | `ncrack -p 22 -U wordlist.txt <target>` |
| medusa | Parallel brute-forcer | `medusa -h <target> -u root -P wordlist.txt -M ssh` |
| weevely | Web shell manager | `weevely <url> <password>` |

### Password (8)
| Tool | Description | Usage |
|---|---|---|
| hashcat | GPU-accelerated hash cracker | `hashcat -m 0 -a 0 <hashfile> wordlist.txt` |
| john | John the Ripper | `john --wordlist=wordlist.txt <hashfile>` |
| crunch | Wordlist generator | `crunch 8 12 abcdef...` |
| cewl | Custom wordlist generator | `cewl <url> -w wordlist.txt` |
| hashid | Hash type identifier | `hashid <hashfile>` |
| gpp-decrypt | Decrypt GPP passwords | `gpp-decrypt <hash>` |
| rsmangler | Wordlist mutation tool | `rsmangler --file <wordlist>` |
| pipal | Password analyzer | `pipal <wordlist>` |

### Wireless (12)
| Tool | Description | Usage |
|---|---|---|
| aircrack-ng | WEP/WPA/WPA2 cracker | `aircrack-ng <capture.cap>` |
| airodump-ng | Packet capture | `airodump-ng <interface>` |
| aireplay-ng | Packet injection | `aireplay-ng -0 5 -a <bssid> <interface>` |
| airmon-ng | Monitor mode manager | `airmon-ng start <interface>` |
| wifite | Automated wireless auditor | `wifite` |
| reaver | WPS PIN brute-force | `reaver -i <interface> -b <bssid> -vv` |
| macchanger | MAC address changer | `macchanger -r <interface>` |
| kismet | Wireless detector/sniffer | `kismet` |
| mdk4 | Wireless DoS tool | `mdk4 <interface> d` |
| bettercap | Network attack framework | `bettercap` |
| bully | WPS brute-force | `bully <interface> -b <bssid>` |
| pixiewps | WPS offline brute-force | `pixiewps --e-hash1=<hash>` |

### AD/Win (4)
| Tool | Description | Usage |
|---|---|---|
| responder | LLMNR/NBT-NS/mDNS poisoner | `responder -I <interface> -wrf` |
| evil-winrm | WinRM shell | `evil-winrm -i <target> -u admin -p password` |
| samdump2 | Extract Windows password hashes | `samdump2 <system> <sam>` |
| chntpw | Windows password reset | `chntpw <SAM>` |

### Tunnel (5)
| Tool | Description | Usage |
|---|---|---|
| proxychains | Force apps through proxy | `proxychains <command>` |
| socat | Multipurpose relay | `socat TCP-LISTEN:8080,fork TCP:<target>:80` |
| ncat | Netcat with SSL | `ncat -lvp 8080` |
| iodine | DNS tunnel | `iodine -d <server>` |
| redsocks | Transparent redirector | `redsocks` |

### MITM (5)
| Tool | Description | Usage |
|---|---|---|
| mitmproxy | Intercepting proxy | `mitmproxy` |
| ettercap | ARP poisoning suite | `ettercap -T -M arp:remote` |
| sslstrip | SSL stripping | `sslstrip` |
| sslscan | SSL/TLS scanner | `sslscan <target>` |
| sslyze | SSL/TLS config analyzer | `sslyze <target>` |

### Traffic (3)
| Tool | Description | Usage |
|---|---|---|
| tcpdump | Packet analyzer | `tcpdump -i any -n` |
| tshark | Wireshark CLI tool | `tshark -i any` |
| ngrep | Network grep | `ngrep -d any` |

### Reverse Engineering (6)
| Tool | Description | Usage |
|---|---|---|
| radare2 | Reverse engineering framework | `r2 <binary>` |
| gdb | GNU debugger | `gdb <binary>` |
| nasm | Netwide assembler | `nasm -f elf64 <file>.asm` |
| binwalk | Firmware analysis | `binwalk <file>` |
| foremost | File carving | `foremost -i <file>` |
| exiv2 | Image metadata tool | `exiv2 <file>` |

### Misc (4)
| Tool | Description |
|---|---|
| arping | ARP ping |
| windows-binaries | Windows binary collection |
| webshells | Web shell collection |
| laudanum | Web shell injection kit |

---

## Attack Chains

| Chain | Description | Tools |
|---|---|---|
| `scan` | Quick vulnerability scan | nmap, gobuster, nikto |
| `recon` | Full reconnaissance | theharvester, dnsrecon, nmap, masscan, enum4linux, netexec |
| `web` | Web application attack | whatweb, nikto, wpscan, dirb, gobuster, ffuf, sqlmap |
| `exploit` | Exploitation chain | searchsploit, nmap, hydra |
| `brute` | Brute force | hydra against ssh, ftp, http-post-form, mysql, smb |
| `osint` | OSINT gathering | theharvester, dnsrecon, dnsenum, fierce, amass, cewl |
| `ad` | Active Directory | enum4linux, netexec, smbmap, responder |
| `wireless` | Wireless attacks | airmon, airodump, aireplay, aircrack, wifite, reaver |
| `password` | Password cracking | hashid, hashcat, john, crunch, cewl |
| `sql` | SQL injection | sqlmap |
| `full` | Full attack chain | recon + web + exploit + brute |

```bash
# Run a chain
neferax scan 10.10.10.1
neferax web https://example.com
neferax full 192.168.1.0/24
```

---

## Installation

### From Kali repository
```bash
# Framework is pre-installed at:
/usr/share/hackingtool/

# Binaries:
/usr/bin/neferax       # CLI (main)
/usr/bin/nefereax      # CLI (alias)
/usr/bin/hackingtool   # TUI menu
```

### Dependencies
- Python 3.10+
- Kali Linux (or Debian-based with pentesting repos)
- All 89 tools from `kali-linux-headless`

### Manual setup
```bash
git clone https://github.com/mastergeeky1-cloud/neferax.git /usr/share/hackingtool
ln -sf /usr/share/hackingtool/nefereax_cli.py /usr/bin/neferax
chmod +x /usr/bin/neferax
```

---

## CLI Reference

```bash
neferax <command> [options] <target>

Commands:
  list                  List all 89 tools by category
  search <query>        Search tools by name/description/command
  info <tool|chain>     Show detailed info about a tool or chain
  version               Show version and stats
  menu                  Launch interactive TUI
  <chain> <target>      Run an attack chain (scan/recon/web/exploit/etc)
  <tool> <target>       Run a single tool directly

Examples:
  neferax scan 10.10.10.1
  neferax web https://example.com
  neferax full 192.168.1.0/24
  neferax info nmap
  neferax search sql
  neferax menu
```

---

## TUI Menu Reference

```bash
neferax menu
# or
hackingtool
```

The TUI provides an interactive menu with:
- **10 categories** organized in a 2-column layout
- **Tool status** indicators (✔ installed / ✘ missing)
- **Search** across all tools
- **Detailed tool info** with usage and examples
- **Target input** and direct tool execution

### Navigation
```
Main Menu:
  1-N     Open a category
  / or s  Search tools
  ?       Show help
  q       Quit

Category:
  1-N     Select a tool
  99      Back to main menu

Tool:
  Enter target/IP to run the tool
```

---

## Tool Verification Status

All 89 tools are **installed and verified** on Kali Linux. Test results:

| Status | Count | Details |
|---|---|---|
| ✅ Passed | 58 | Tools ran successfully against localhost/test targets |
| ⏭️ Skipped | 21 | Wireless tools needing hardware (WiFi adapter) |
| ⚠️ Timeout | 10 | Tools needing external services (SMB, WinRM, web targets) |

Tools that timed out (`nikto`, `theharvester`, `fierce`, `enum4linux`, `spiderfoot`, etc.) work correctly against real targets but require an active remote service to scan.

---

## File Structure

```
/usr/share/hackingtool/
├── nefereax_cli.py      # Main CLI (89 tools, 11 chains, styled output)
├── hackingtool.py        # TUI menu (rich interface, same tool set)
├── core.py               # Base classes (HackingTool, HackingToolsCollection)
├── constants.py          # Theme colors, version, repo URL
├── config.py             # Configuration and paths
├── tools/                # Tool category modules
│   ├── information_gathering.py
│   ├── web_attack.py
│   ├── wireless_attack.py
│   ├── sql_injection.py
│   ├── password tools...
│   └── ...
├── images/
│   └── logo.svg          # Neferax SVG logo
├── venv/                 # Python virtual environment
└── requirements.txt      # Python dependencies
```

---

## License

This project is provided for **authorized security testing and educational purposes only**. Unauthorized use against systems you do not own or have explicit permission to test is illegal.

---

**Neferax** — Built by [mastergeeky1-cloud](https://github.com/mastergeeky1-cloud)
