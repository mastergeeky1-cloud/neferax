#!/usr/bin/env python3
import sys
if sys.version_info < (3, 10):
    print(f"[ERROR] Python 3.10+ required (have {sys.version_info.major}.{sys.version_info.minor})")
    sys.exit(1)

import os, subprocess, socket, platform, datetime, random, webbrowser
from itertools import zip_longest
from shutil import which

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich import box
from rich.rule import Rule

console = Console()

VERSION = "2.0.0"

# ── Tool definition ─────────────────────────────────────────────────────────
class SystemTool:
    def __init__(self, title, description, binary, usage, category="", tags=None):
        self.title = title
        self.description = description
        self.binary = binary
        self.usage = usage
        self.category = category
        self.tags = tags or []

    @property
    def installed(self):
        return which(self.binary) is not None

    def run(self, target=""):
        cmd = self.usage.replace("<target>", target).replace("<domain>", target).replace("<url>", target)
        console.print(f"[bold cyan]> {cmd}[/bold cyan]")
        try:
            subprocess.run(cmd, shell=True)
        except KeyboardInterrupt:
            pass
        Prompt.ask("[dim]Press Enter to return[/dim]", default="")

class ToolCategory:
    def __init__(self, title, icon, tools):
        self.title = title
        self.icon = icon
        self.tools = tools

# ── Tool categories ────────────────────────────────────────────────────────

TOOLS_BY_CAT = {
    "Recon": ["nmap","masscan","netdiscover","arp-scan","theharvester","dnsrecon",
              "dnsenum","fierce","amass","dmitry","enum4linux","netexec","smbmap",
              "nbtscan","hping3","fping","ike-scan","recon-ng","spiderfoot","whois",
              "httpx","subfinder","naabu"],
    "Web": ["nikto","whatweb","wpscan","skipfish","wafw00f","gobuster","dirb",
            "ffuf","wfuzz","sqlmap","commix","lbd","gospider"],
    "Exploit": ["searchsploit","metasploit","hydra","ncrack","medusa","weevely"],
    "Password": ["hashcat","john","crunch","cewl","hashid","rsmangler","pipal"],
    "Wireless": ["aircrack-ng","airodump-ng","aireplay-ng","airmon-ng","wifite",
                 "reaver","macchanger","kismet","mdk4","bettercap","bully"],
    "AD/Win": ["responder","evil-winrm","samdump2","chntpw","bloodhound","certipy","kerbrute"],
    "Cloud": ["s3scanner","prowler","scoutsuite","tfsec","checkov","cloudsploit"],
    "Container": ["trivy","kubectl","kubescape","kube-hunter","dockle","hadolint"],
    "Mobile": ["apktool","dex2jar","jadx","objection","mobsf"],
    "Tunnel": ["proxychains","socat","ncat","iodine","redsocks"],
    "MITM": ["mitmproxy","ettercap","sslstrip","sslscan","sslyze"],
    "Traffic": ["tcpdump","tshark","ngrep"],
    "Reverse": ["radare2","gdb","nasm","binwalk","foremost","exiv2"],
    "pwntools": ("Pwntools","Exploit development library","pwntools <binary>"),
    "PE": ["pecheck","pe-sieve","floss","capa","peframe","detect-it-easy"],
    "Memory": ["volatility","volatility3","avml","lime","scanmem","memdump","gcore"],
    "Scanning": ["rustscan","zmap","zgrab","crackmapexec","impacket"],
    "Attacking": ["mimikatz","msfvenom","chisel","ligolo-ng","beef"],
}

TOOL_META = {
    # recon
    "nmap": ("Network Mapper (nmap)","Network discovery & security auditing","nmap <target>"),
    "masscan": ("Masscan","Fast internet port scanner","masscan --rate=1000 -p1-65535 <target>"),
    "netdiscover": ("Netdiscover","Passive/active ARP scanner","netdiscover -r <target>"),
    "arp-scan": ("ARP-Scan","ARP scan local network","arp-scan --localnet"),
    "theharvester": ("theHarvester","OSINT: emails, subdomains, IPs","theHarvester -d <domain> -b all"),
    "dnsrecon": ("DNSRecon","DNS enumeration tool","dnsrecon -d <target> -t std"),
    "dnsenum": ("DNSEnum","DNS enumeration utility","dnsenum <target>"),
    "fierce": ("Fierce","DNS reconnaissance","fierce --domain <domain>"),
    "amass": ("Amass","Attack surface mapping","amass enum -d <domain>"),
    "dmitry": ("DMitry","Deepmagic information gathering","dmitry <target>"),
    "enum4linux": ("Enum4linux","Windows/Samba enumeration","enum4linux -a <target>"),
    "netexec": ("NetExec","Network execution suite (SMB/WinRM)","netexec smb <target>"),
    "smbmap": ("SMBMap","SMB share enumeration","smbmap -H <target>"),
    "nbtscan": ("NBTScan","NetBIOS name scanner","nbtscan <target>"),
    "hping3": ("Hping3","Packet crafting & analysis","hping3 -c 4 <target>"),
    "fping": ("Fping","Ping sweep tool","fping -asg <target>"),
    "ike-scan": ("IKE-Scan","IKE VPN scanning","ike-scan <target>"),
    "recon-ng": ("Recon-ng","Web reconnaissance framework","recon-ng"),
    "spiderfoot": ("SpiderFoot","OSINT automation","spiderfoot -s <target>"),
    "whois": ("Whois","Domain registration lookup","whois <target>"),
    # web
    "nikto": ("Nikto","Web server scanner","nikto -h <target>"),
    "whatweb": ("WhatWeb","Web technology identifier","whatweb -v <target>"),
    "wpscan": ("WPScan","WordPress security scanner","wpscan --url <target> --enumerate vp,vt,u"),
    "skipfish": ("Skipfish","Web app security scanner","skipfish -o /tmp/skipfish <target>"),
    "wafw00f": ("Wafw00f","WAF detection fingerprinting","wafw00f <target>"),
    "gobuster": ("Gobuster","Directory/file brute-forcer","gobuster dir -u <target> -w /usr/share/wordlists/dirb/common.txt"),
    "dirb": ("Dirb","Web content scanner","dirb <target>"),
    "ffuf": ("Ffuf","Fast web fuzzer","ffuf -w /usr/share/wordlists/dirb/common.txt -u <target>/FUZZ"),
    "wfuzz": ("Wfuzz","Web fuzzer","wfuzz -w /usr/share/wordlists/wfuzz/general/common.txt <target>"),
    "sqlmap": ("SQLMap","SQL injection automation","sqlmap -u <target> --batch"),
    "commix": ("Commix","Command injection exploiter","commix --url=<target>"),
    "lbd": ("LBD","Load balancing detector","lbd <domain>"),
    # exploit
    "searchsploit": ("Searchsploit","Exploit-DB search tool","searchsploit <query>"),
    "metasploit": ("Metasploit Framework","Metasploit framework console","msfconsole -q"),
    "hydra": ("Hydra","Online password brute-forcer","hydra -l root -P /usr/share/wordlists/rockyou.txt.gz <target> <service>"),
    "ncrack": ("Ncrack","Network authentication cracker","ncrack -p 22 -U /usr/share/wordlists/rockyou.txt.gz <target>"),
    "medusa": ("Medusa","Parallel brute-forcer","medusa -h <target> -u root -P /usr/share/wordlists/rockyou.txt.gz -M ssh"),
    "weevely": ("Weevely","Web shell manager","weevely <url> <password>"),
    # password
    "hashcat": ("Hashcat","GPU-accelerated hash cracker","hashcat -m 0 -a 0 <hashfile> /usr/share/wordlists/rockyou.txt.gz"),
    "john": ("John the Ripper","Hash cracker","john --wordlist=/usr/share/wordlists/rockyou.txt.gz <hashfile>"),
    "crunch": ("Crunch","Wordlist generator","crunch 8 12 abcdefghijklmnopqrstuvwxyz"),
    "cewl": ("Cewl","Custom wordlist generator","cewl <url> -w wordlist.txt"),
    "hashid": ("HashID","Hash type identifier","hashid <hashfile>"),
    "rsmangler": ("RsMangler","Wordlist mutation","rsmangler --file <wordlist>"),
    "pipal": ("Pipal","Password analyzer","pipal <wordlist>"),
    # wireless
    "aircrack-ng": ("Aircrack-ng","WEP/WPA/WPA2 cracker","aircrack-ng <capture.cap>"),
    "airodump-ng": ("Airodump-ng","Wireless packet capture","airodump-ng <interface>"),
    "aireplay-ng": ("Aireplay-ng","Wireless packet injection","aireplay-ng -0 5 -a <bssid> <interface>"),
    "airmon-ng": ("Airmon-ng","Monitor mode manager","airmon-ng start <interface>"),
    "wifite": ("Wifite","Automated wireless auditor","wifite"),
    "reaver": ("Reaver","WPS PIN brute-force","reaver -i <interface> -b <bssid> -vv"),
    "macchanger": ("Macchanger","MAC address changer","macchanger -r <interface>"),
    "kismet": ("Kismet","Wireless detector/sniffer","kismet"),
    "mdk4": ("Mdk4","Wireless DoS tool","mdk4 <interface> d"),
    "bettercap": ("Bettercap","Network attack framework","bettercap -eval 'net.probe on; net.show'"),
    "bully": ("Bully","WPS brute-force (reaver alt)","bully <interface> -b <bssid>"),
    # ad/win
    "responder": ("Responder","LLMNR/NBT-NS/mDNS poisoner","responder -I <interface> -wrf"),
    "evil-winrm": ("Evil-WinRM","WinRM shell","evil-winrm -i <target> -u admin -p password"),
    "samdump2": ("Samdump2","Extract Windows password hashes","samdump2 <system> <sam>"),
    "chntpw": ("Chntpw","Windows password reset utility","chntpw <SAM>"),
    # tunnel
    "proxychains": ("Proxychains","Force apps through proxy","proxychains <command>"),
    "socat": ("Socat","Multipurpose relay","socat TCP-LISTEN:8080,fork TCP:<target>:80"),
    "ncat": ("Ncat","Netcat with SSL","ncat -lvp 8080"),
    "iodine": ("Iodine","DNS tunnel","iodine -d <server>"),
    "redsocks": ("Redsocks","Transparent redirector","redsocks"),
    # mitm
    "mitmproxy": ("Mitmproxy","Intercepting proxy","mitmproxy"),
    "ettercap": ("Ettercap","ARP poisoning suite","ettercap -T -M arp:remote /<gateway>// /<target>//"),
    "sslstrip": ("SSLstrip","SSL stripping tool","sslstrip"),
    "sslscan": ("SSLscan","SSL/TLS scanner","sslscan <target>"),
    "sslyze": ("SSLyze","SSL/TLS config analyzer","sslyze <target>"),
    # traffic
    "tcpdump": ("Tcpdump","Packet analyzer","tcpdump -i any -n"),
    "tshark": ("TShark","Wireshark CLI tool","tshark -i any"),
    "ngrep": ("Ngrep","Network grep","ngrep -d any"),
    # reverse
    "radare2": ("Radare2","Reverse engineering framework","r2 <binary>"),
    "gdb": ("GDB","GNU debugger","gdb <binary>"),
    "nasm": ("NASM","Netwide assembler","nasm -f elf64 <file>.asm"),
    "binwalk": ("Binwalk","Firmware analysis","binwalk <file>"),
    "foremost": ("Foremost","File carving","foremost -i <file>"),
    "exiv2": ("Exiv2","Image metadata tool","exiv2 <file>"),
    # cloud
    "s3scanner": ("S3Scanner","Find open S3 buckets","s3scanner -bucket <target>"),
    "prowler": ("Prowler","AWS security auditing","prowler <target>"),
    "scoutsuite": ("ScoutSuite","Multi-cloud security scanner","scoutsuite <target>"),
    "tfsec": ("Tfsec","Terraform security scanner","tfsec <dir>"),
    "checkov": ("Checkov","IaC misconfiguration scanner","checkov -d <dir>"),
    "cloudsploit": ("CloudSploit","Cloud security scanning","cloudsploit <target>"),
    # container
    "trivy": ("Trivy","Container vulnerability scanner","trivy image <target>"),
    "kubectl": ("Kubectl","Kubernetes CLI","kubectl get pods"),
    "kubescape": ("Kubescape","K8s security scanning","kubescape scan <target>"),
    "kube-hunter": ("Kube-Hunter","K8s penetration testing","kube-hunter"),
    "dockle": ("Dockle","Dockerfile linter","dockle <image>"),
    "hadolint": ("Hadolint","Dockerfile linting","hadolint <dockerfile>"),
    # mobile
    "apktool": ("Apktool","APK reverse engineering","apktool d <apk>"),
    "dex2jar": ("Dex2Jar","DEX to JAR converter","d2j-dex2jar <dex>"),
    "jadx": ("Jadx","Dex to Java decompiler","jadx <apk>"),
    "objection": ("Objection","Runtime mobile exploration","objection -g <package> explore"),
    "mobsf": ("MobSF","Mobile security framework","mobsf"),
    # advanced
    "bloodhound": ("BloodHound","AD attack path mapping","bloodhound"),
    "certipy": ("Certipy","AD CS exploitation","certipy find -u <user> -p <pass> -dc-ip <target>"),
    "kerbrute": ("Kerbrute","Kerberos user enumeration","kerbrute userenum -d <domain> <wordlist> <target>"),
    "gospider": ("GoSpider","Web spider/crawler","gospider -s <target>"),
    "httpx": ("Httpx","HTTP probing toolkit","httpx -u <target>"),
    "subfinder": ("Subfinder","Subdomain discovery","subfinder -d <domain>"),
    "naabu": ("Naabu","Fast port scanner","naabu -host <target>"),
    # binary
    "strings": ("Strings","Extract strings from binaries","strings <binary>"),
    "xxd": ("Xxd","Hex dump and reverse","xxd <binary>"),
    "objdump": ("Objdump","Disassemble object files","objdump -d <binary>"),
    "readelf": ("Readelf","ELF file analysis","readelf -a <binary>"),
    "strace": ("Strace","System call tracer","strace -f -o trace.log <command>"),
    "ltrace": ("Ltrace","Library call tracer","ltrace -o trace.log <command>"),
    "nm": ("Nm","Symbol listing","nm <binary>"),
    "strip": ("Strip","Strip symbols","strip <binary>"),
    "objcopy": ("Objcopy","Copy/manipulate objects","objcopy <infile> <outfile>"),
    "ropper": ("Ropper","ROP gadget finder","ropper --file <binary>"),
    "pwntools": ("Pwntools","Exploit development library","pwntools"),
    # pe
    "pecheck": ("Pecheck","PE file checker","pecheck <exe>"),
    "pe-sieve": ("Pe-Sieve","PE analysis/malware detection","pe-sieve /pid <pid>"),
    "floss": ("Floss","FireEye Obfuscated String Solver","floss <exe>"),
    "capa": ("Capa","Binary capability analyzer","capa <exe>"),
    "peframe": ("Peframe","PE analysis framework","peframe <exe>"),
    "detect-it-easy": ("Detect It Easy","File type identifier","diec <exe>"),
    # memory
    "volatility": ("Volatility","Memory forensics framework","volatility -f <memory.dump> --profile=<profile>"),
    "volatility3": ("Volatility3","Memory forensics v3","vol -f <memory.dump>"),
    "avml": ("Avml","Acquire Volatile Memory Linux","avml <output.lime>"),
    "lime": ("Lime","Linux Memory Extractor","lime-forensics <output.mem>"),
    "scanmem": ("Scanmem","Memory scanner/editor","scanmem <pid>"),
    "memdump": ("Memdump","Process memory dumper","memdump <pid>"),
    "gcore": ("Gcore","Core dump generator","gcore <pid>"),
    # scanning
    "rustscan": ("RustScan","Ultra-fast Rust port scanner","rustscan -a <target>"),
    "zmap": ("ZMap","Internet-wide scanner","zmap -p 443 <target>"),
    "zgrab": ("ZGrab","Application-layer scanner","zgrab --port 443 --tls <target>"),
    "crackmapexec": ("CrackMapExec","Network attack suite","crackmapexec smb <target>"),
    "impacket": ("Impacket","AD protocol toolkit","impacket-GetNPUsers -dc-ip <target> <domain>/"),
    # attacking
    "mimikatz": ("Mimikatz","Windows credential extraction","mimikatz"),
    "msfvenom": ("Msfvenom","Metasploit payload generator","msfvenom -p <payload> LHOST=<target> LPORT=4444"),
    "chisel": ("Chisel","Fast TCP/UDP tunnel","chisel client <target>:<port>"),
    "ligolo-ng": ("Ligolo-ng","Tunneling proxy","ligolo-ng -connect <target>:<port>"),
    "beef": ("BeEF","Browser exploitation framework","beef-xss"),
}

def build_category(name, icon, tool_names):
    tools = []
    for bn in tool_names:
        meta = TOOL_META.get(bn)
        if meta:
            t = SystemTool(meta[0], meta[1], bn, meta[2], name)
            tools.append(t)
    return ToolCategory(name, icon, tools)

CATEGORIES = [
    build_category("Recon", "🔍", TOOLS_BY_CAT["Recon"]),
    build_category("Web", "🌐", TOOLS_BY_CAT["Web"]),
    build_category("Exploit", "⚡", TOOLS_BY_CAT["Exploit"]),
    build_category("Password", "🔑", TOOLS_BY_CAT["Password"]),
    build_category("Wireless", "📶", TOOLS_BY_CAT["Wireless"]),
    build_category("AD/Win", "🏢", TOOLS_BY_CAT["AD/Win"]),
    build_category("Tunnel", "🔌", TOOLS_BY_CAT["Tunnel"]),
    build_category("MITM", "🕵️", TOOLS_BY_CAT["MITM"]),
    build_category("Traffic", "📡", TOOLS_BY_CAT["Traffic"]),
    build_category("Reverse", "🔁", TOOLS_BY_CAT["Reverse"]),
]

def clear():
    os.system("clear")

QUOTES = [
    '"The quieter you become, the more you can hear."',
    '"Offense informs defense."',
    '"There is no patch for human stupidity."',
    '"In God we trust. All others we monitor."',
    '"Trust is a vulnerability."',
    '"Darkness is the best disguise."',
    '"The only secure system is the one that is powered off."',
]

BANNER = r"""
   _____  _____  _____  _____  _____   _____          ___
  / ____|/ ____|/ ____|/ ____||  __ \ / ____|   /\   | \ |
 | (___ | |    | |    | (___  | |__) | |       /  \  |  \|
  \___ \| |    | |     \___ \ |  _  /| |      / /\ \ | . |
  ____) | |____| |____ ____) || | \ \| |____ / ____ \| |\|
 |_____/ \_____|\_____|_____/ |_|  \_\\_____/_/    \_\_| \|
"""

def build_header():
    info = {}
    try:
        with open("/etc/os-release") as f:
            for l in f:
                if l.startswith("PRETTY_NAME="):
                    info["os"] = l.split("=",1)[1].strip().strip('"')
                    break
    except: info["os"] = f"{platform.system()} {platform.release()}"
    info["kernel"] = platform.version()[:40]
    info["user"] = os.environ.get("USER","unknown")
    info["host"] = socket.gethostname()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0); s.connect(("10.254.254.254",1))
        info["ip"] = s.getsockname()[0]; s.close()
    except: info["ip"] = "127.0.0.1"
    info["time"] = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M")
    info["tools"] = f"{len(TOOL_META)} tools · {len(CATEGORIES)} categories"

    stat_lines = [
        ("os      ", info["os"][:34]),
        ("kernel  ", info["kernel"][:34]),
        ("user    ", f"{info['user']} @ {info['host'][:20]}"),
        ("ip      ", info["ip"]),
        ("tools   ", info["tools"]),
        ("session ", info["time"]),
        ("", ""),
        ("status  ", "✔ READY"),
    ]

    grid = Table.grid(padding=0)
    grid.add_column("art", no_wrap=True)
    grid.add_column("sep", no_wrap=True)
    grid.add_column("lbl", no_wrap=True)
    grid.add_column("val", no_wrap=True)

    banner_lines = [l for l in BANNER.split("\n") if l.strip()]
    for art_line, (lbl_text, val_text) in zip(banner_lines, stat_lines):
        grid.add_row(
            Text(art_line, style="bold red"),
            Text("  |  ", style="dim red"),
            Text(lbl_text, style="dim red"),
            Text(val_text, style="bright_red"),
        )

    quote = random.choice(QUOTES)
    body = Table.grid(padding=(0,0))
    body.add_column()
    body.add_row(grid)
    body.add_row(Text(""))
    body.add_row(Text(f"  {quote}", style="italic dim red"))
    body.add_row(Text("  \u2620  For authorized security testing only", style="bold dim red"))

    return Panel(
        body,
        title=f"[bold bright_red][ Neferax v{VERSION} ][/bold bright_red]",
        title_align="left",
        subtitle=f"[dim][ {info['time']} ][/dim]",
        subtitle_align="right",
        border_style="bright_red",
        box=box.HEAVY,
        padding=(0,1),
    )

def show_help():
    console.print(Panel(Text.assemble(
        ("\n  Main Menu\n", "bold white"),
        ("  ─────────────────\n", "dim"),
        ("  1-10   ", "bold cyan"),("open a category\n", "white"),
        ("  / or s ","bold cyan"),("search tools\n", "white"),
        ("  ?      ","bold cyan"),("show this help\n", "white"),
        ("  q      ","bold cyan"),("quit Neferax\n", "white"),
        ("\n  Inside a Category\n", "bold white"),
        ("  ─────────────────\n", "dim"),
        ("  1-N    ", "bold cyan"),("select a tool\n", "white"),
        ("  99     ", "bold cyan"),("back to main menu\n", "white"),
        ("\n  Running a Tool\n", "bold white"),
        ("  ─────────────────\n", "dim"),
        ("  Enter target/IP or leave blank to see usage\n", "white"),
        ("  Enter tool-specific params when prompted\n", "white"),
    ), title="[bold bright_red] ? Quick Help [/bold bright_red]", border_style="bright_red", box=box.ROUNDED, padding=(0,2)))
    Prompt.ask("[dim]Press Enter[/dim]", default="")

def show_category(cat):
    clear()
    console.print(Panel(Text(f"[bold red]{cat.icon}  {cat.title}[/bold red]"), border_style="bright_red"))
    table = Table(border_style="red", box=box.ROUNDED, show_header=True)
    table.add_column("#", style="bold red", width=4, justify="right")
    table.add_column("Tool", style="bold white")
    table.add_column("Status", style="dim", width=10)
    table.add_column("Description", style="dim white")
    for i, t in enumerate(cat.tools, 1):
        status = "[green]✔[/green]" if t.installed else "[red]✘[/red]"
        desc = t.description[:50]
        table.add_row(str(i), t.title, status, desc)
    console.print(table)
    console.print("  [dim]99 Back[/dim]")

    while True:
        choice = Prompt.ask("  [bold red]> ")
        if choice == "99": return
        try:
            idx = int(choice)
            if 1 <= idx <= len(cat.tools):
                run_tool(cat.tools[idx-1])
        except ValueError: pass

def run_tool(tool):
    clear()
    console.print(Panel(Text(f"[bold red]{tool.title}[/bold red]\n\n[dim]{tool.description}[/dim]", style="white"), border_style="bright_red"))
    if not tool.installed:
        console.print(f"[yellow]Warning: '{tool.binary}' not found on system. Install it first: sudo apt install {tool.binary}[/yellow]")
    console.print(f"\n[bold cyan]Usage:[/bold cyan] {tool.usage}")
    console.print(f"\n[bold cyan]Examples:[/bold cyan]")
    for ex in _examples(tool.binary):
        console.print(f"  [dim]{ex}[/dim]")
    target = Prompt.ask("\n[bold red]Enter target[/bold red]", default="")
    tool.run(target)

def _examples(binary):
    ex = {
        "nmap":["nmap -sV 10.10.10.1","nmap -sC -sV -O 10.10.10.1"],
        "gobuster":["gobuster dir -u https://example.com -w /usr/share/wordlists/dirb/common.txt"],
        "nikto":["nikto -h https://example.com"],
        "sqlmap":["sqlmap -u 'http://example.com/page?id=1' --batch"],
        "hydra":["hydra -l admin -P wordlist.txt 10.10.10.1 ssh"],
        "dirb":["dirb http://example.com"],
        "ffuf":["ffuf -w wordlist.txt -u https://example.com/FUZZ"],
        "whatweb":["whatweb https://example.com"],
        "wpscan":["wpscan --url https://example.com"],
        "masscan":["masscan -p1-65535 10.10.10.0/24 --rate=1000"],
    }
    return ex.get(binary, [f"{binary} --help"])

def tool_search():
    query = Prompt.ask("[bold red]Search[/bold red]").strip().lower()
    if not query: return
    results = []
    for cat in CATEGORIES:
        for t in cat.tools:
            if query in t.title.lower() or query in t.description.lower() or query in t.binary.lower():
                results.append((cat.title, t.title, t.description))
    if not results:
        console.print("[yellow]No tools found.[/yellow]")
    else:
        table = Table(title=f'Search: "{query}"', title_style="bold red", border_style="bright_red", box=box.SIMPLE)
        table.add_column("Category", style="red")
        table.add_column("Tool", style="bold red")
        table.add_column("Description", style="dim white")
        for cat, tool, desc in results:
            table.add_row(cat, tool, desc)
        console.print(table)
    Prompt.ask("[dim]Press Enter[/dim]", default="")

def build_menu():
    clear()
    console.print(build_header())

    mid = (len(CATEGORIES) + 1) // 2
    left = list(enumerate(CATEGORIES[:mid], 1))
    right = list(enumerate(CATEGORIES[mid:], mid + 1))

    grid = Table.grid(padding=(0,1), expand=True)
    grid.add_column("ln", justify="right", style="bold red", width=4)
    grid.add_column("li", width=3)
    grid.add_column("lt", style="red", ratio=1, no_wrap=True)
    grid.add_column("gap", width=3)
    grid.add_column("rn", justify="right", style="bold red", width=4)
    grid.add_column("ri", width=3)
    grid.add_column("rt", style="red", ratio=1, no_wrap=True)

    for (li, lcat), r in zip_longest(left, right, fillvalue=None):
        if r:
            ri, rcat = r
            grid.add_row(str(li), lcat.icon, lcat.title, "", str(ri), rcat.icon, rcat.title)
        else:
            grid.add_row(str(li), lcat.icon, lcat.title, "", "", "", "")

    console.print(Panel(grid, title="[bold red] Select a Category [/bold red]", border_style="bright_red", box=box.ROUNDED, padding=(0,1)))

    console.print(Rule(style="dim red"))
    console.print("  [dim cyan]/[/dim cyan] [dim cyan]search[/dim cyan]  [dim cyan]?[/dim cyan] [dim cyan]help[/dim cyan]  [dim cyan]q[/dim cyan] [dim cyan]quit[/dim cyan]")

    choice = Prompt.ask("  [bold red]> ")

    if choice == "q":
        console.print("[bold red]Darkness prevails. Exiting...[/bold red]")
        sys.exit(0)
    elif choice == "?":
        show_help(); return
    elif choice in ("/", "s"):
        tool_search(); return
    try:
        idx = int(choice)
        if 1 <= idx <= len(CATEGORIES):
            show_category(CATEGORIES[idx-1])
    except ValueError: pass

def main():
    while True:
        try:
            build_menu()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bold red]Darkness prevails. Exiting...[/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    main()
