#!/usr/bin/env python3
import os, sys, subprocess, signal
from datetime import datetime

V = "2.0.0"
R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'; C = '\033[96m'
W = '\033[97m'; D = '\033[2m'; L = '\033[1m'; X = '\033[0m'
BW = 56

def S(text, style=L): return f"{style}{text}{X}"

LOGO_LINES = [
    " _   _ ______ ______ ______ _____            __   __",
    "| \\ | |  ____|  ____|  ____|  __ \\     /\\    \\ \\ / /",
    "|  \\| | |__  | |__  | |__  | |__) |   /  \\    \\ V /",
    "| . ` |  __| |  __| |  __| |  _  /   / /\\ \\    > <",
    "| |\\  | |____| |    | |____| | \\ \\  / ____ \\  / . \\",
    "|_| \\_|______|_|    |______|_|  \\_\\/_/    \\_\\/_/ \\_\\",
]

LOGO = ""
for i, line in enumerate(LOGO_LINES):
    side = R
    LOGO += f"  {side}\u2551  {S(line)}{' '*(BW - len(line) - 4)}{side}\u2551{X}\n"

def logo():
    os.system('clear')
    print(f"  {R}\u2554{'\u2550'*BW}\u2557{X}")
    print(LOGO, end='')
    print(f"  {R}\u255a{'\u2550'*BW}\u255d{X}")
    print(f"  {D}\u2554{'\u2550'*BW}\u2557{X}")
    sub = f"Dark Security Framework  v{V}  |  {S(f'{len(TOOLS)} tools',C)}  |  {S(f'{len(CHAINS)} chains',Y)}"
    print(f"  {D}\u2551  {sub}{' '*(BW - len(sub) - 4)}{D}\u2551{X}")
    print(f"  {D}\u255a{'\u2550'*BW}\u255d{X}")
    print()

def box_start(title=None, sep=False):
    if title:
        print(f"  {R}\u2554{'\u2550'*BW}\u2557{X}")
        print(f"  {R}\u2551  {S(title)}{' '*(BW - len(title) - 4)}{R}\u2551{X}")
    else:
        print(f"  {R}\u2554{'\u2550'*BW}\u2557{X}")
    if sep:
        print(f"  {R}\u2560{'\u2550'*BW}\u2563{X}")

def box_end():
    print(f"  {R}\u255a{'\u2550'*BW}\u255d{X}")

def box_line(text, style=W, pad=True):
    p = 2 if pad else 0
    content = f"{style}{text}{X}" if style else text
    print(f"  {R}\u2551{' '*p}{content}{' '*(BW - len(text) - p)}{R}\u2551{X}")

def log(lvl, msg):
    sym = {"+":f"{G}\u2503 [+] \u2503{X}", "-":f"{R}\u2503 [-] \u2503{X}",
           "*":f"{C}\u2503 [*] \u2503{X}", "!":f"{Y}\u2503 [!] \u2503{X}"}
    print(f"  {D}\u2503{X} {sym.get(lvl,lvl).ljust(8)} {msg}")

def run(cmd, desc=None):
    print(f"  {R}\u2554{'\u2550'*BW}\u2557{X}")
    if desc:
        print(f"  {R}\u2551  {S(desc)}{' '*(BW - len(desc) - 4)}{R}\u2551{X}")
        print(f"  {R}\u2551  {D}{cmd}{X}{' '*(BW - len(cmd) - 4)}{R}\u2551{X}")
    else:
        print(f"  {R}\u2551  {D}{cmd}{X}{' '*(BW - len(cmd) - 4)}{R}\u2551{X}")
    print(f"  {R}\u255a{'\u2550'*BW}\u255d{X}")
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
        for line in p.stdout:
            print(f"  {W}  {line}", end='')
        p.wait()
        log("+" if p.returncode == 0 else "!", f"Exit: {p.returncode}")
        return p.returncode
    except KeyboardInterrupt:
        log("!", "Interrupted")
        return -1
    except Exception as e:
        log("-", str(e))
        return -1

TOOLS = {}

def tool(name, cmd, cat="misc", desc=""):
    TOOLS[name] = {"cmd": cmd, "cat": cat, "desc": desc}

# ── RECON ──
tool("nmap","nmap <target>","recon","Network discovery & security auditing")
tool("masscan","masscan --rate=1000 -p1-65535 <target>","recon","Fast internet port scanner")
tool("netdiscover","netdiscover -r <target>","recon","Passive/active ARP scanner")
tool("arp-scan","arp-scan --localnet","recon","ARP scan local network")
tool("theharvester","theHarvester -d <domain> -b all","recon","Email, subdomain & name OSINT")
tool("dnsrecon","dnsrecon -d <target> -t std","recon","DNS enumeration tool")
tool("dnsenum","dnsenum <target>","recon","DNS enumeration utility")
tool("fierce","fierce --domain <domain>","recon","DNS reconnaissance")
tool("amass","amass enum -d <domain>","recon","Attack surface mapping")
tool("dmitry","dmitry <target>","recon","Deepmagic info gathering")
tool("enum4linux","enum4linux -a <target>","recon","Windows/Samba enumeration")
tool("netexec","netexec smb <target>","recon","Network execution suite")
tool("smbmap","smbmap -H <target>","recon","SMB share enumeration")
tool("nbtscan","nbtscan <target>","recon","NetBIOS name scanner")
tool("onesixtyone","onesixtyone <target>","recon","SNMP scanner")
tool("snmpcheck","snmpcheck -t <target>","recon","SNMP enumeration")
tool("hping3","hping3 -c 4 <target>","recon","Packet crafting & analysis")
tool("fping","fping -asg <target>","recon","Ping sweep tool")
tool("ike-scan","ike-scan <target>","recon","IKE VPN scanning")
tool("dnschef","dnschef","recon","DNS proxy/spoofer")
tool("recon-ng","recon-ng","recon","Web reconnaissance framework")
tool("spiderfoot","spiderfoot -s <target>","recon","OSINT automation")
tool("whois","whois <target>","recon","Domain registration lookup")

# ── WEB ──
tool("nikto","nikto -h <target>","web","Web server scanner")
tool("whatweb","whatweb -v <target>","web","Web technology identifier")
tool("wpscan","wpscan --url <target> --enumerate vp,vt,u","web","WordPress security scanner")
tool("skipfish","skipfish -o /tmp/skipfish <target>","web","Web app security scanner")
tool("wafw00f","wafw00f <target>","web","WAF detection fingerprinting")
tool("gobuster","gobuster dir -u <target> -w /usr/share/wordlists/dirb/common.txt","web","Directory/file brute-forcer")
tool("dirb","dirb <target>","web","Web content scanner")
tool("ffuf","ffuf -w /usr/share/wordlists/dirb/common.txt -u <target>/FUZZ","web","Fast web fuzzer")
tool("wfuzz","wfuzz -w /usr/share/wordlists/wfuzz/general/common.txt <target>","web","Web fuzzer")
tool("sqlmap","sqlmap -u <target> --batch","web","SQL injection automation")
tool("commix","commix --url=<target>","web","Command injection exploiter")
tool("lbd","lbd <domain>","web","Load balancing detector")

# ── EXPLOIT ──
tool("searchsploit","searchsploit <query>","exploit","Exploit-DB search tool")
tool("metasploit","msfconsole -q","exploit","Metasploit framework console")
tool("set","setoolkit","exploit","Social Engineer Toolkit")
tool("hydra","hydra -l root -P /usr/share/wordlists/rockyou.txt.gz <target> <service>","exploit","Online password brute-forcer")
tool("ncrack","ncrack -p 22 -U /usr/share/wordlists/rockyou.txt.gz <target>","exploit","Network authentication cracker")
tool("medusa","medusa -h <target> -u root -P /usr/share/wordlists/rockyou.txt.gz -M ssh","exploit","Parallel brute-forcer")
tool("weevely","weevely <url> <password>","exploit","Web shell manager")

# ── PASSWORD ──
tool("hashcat","hashcat -m 0 -a 0 <hashfile> /usr/share/wordlists/rockyou.txt.gz","password","GPU-accelerated hash cracker")
tool("john","john --wordlist=/usr/share/wordlists/rockyou.txt.gz <hashfile>","password","John the Ripper")
tool("crunch","crunch 8 12 abcdefghijklmnopqrstuvwxyz","password","Wordlist generator")
tool("cewl","cewl <url> -w wordlist.txt","password","Custom wordlist generator")
tool("hashid","hashid <hashfile>","password","Hash type identifier")
tool("gpp-decrypt","gpp-decrypt <hash>","password","Decrypt GPP passwords")
tool("rsmangler","rsmangler --file <wordlist>","password","Wordlist mutation tool")
tool("pipal","pipal <wordlist>","password","Password analyzer")

# ── WIRELESS ──
tool("aircrack","aircrack-ng <capture.cap>","wireless","WEP/WPA/WPA2 cracker")
tool("airodump","airodump-ng <interface>","wireless","Packet capture")
tool("aireplay","aireplay-ng -0 5 -a <bssid> <interface>","wireless","Packet injection")
tool("airmon","airmon-ng start <interface>","wireless","Monitor mode manager")
tool("wifite","wifite","wireless","Automated wireless auditor")
tool("reaver","reaver -i <interface> -b <bssid> -vv","wireless","WPS PIN brute-force")
tool("macchanger","macchanger -r <interface>","wireless","MAC address changer")
tool("kismet","kismet","wireless","Wireless detector/sniffer")
tool("mdk4","mdk4 <interface> d","wireless","Wireless DoS tool")
tool("bettercap","bettercap -eval 'net.probe on; net.show'","wireless","Network attack framework")
tool("bully","bully <interface> -b <bssid>","wireless","WPS brute-force")
tool("pixiewps","pixiewps --e-hash1=<hash>","wireless","WPS offline brute-force")

# ── AD/WIN ──
tool("responder","responder -I <interface> -wrf","ad","LLMNR/NBT-NS/mDNS poisoner")
tool("evil-winrm","evil-winrm -i <target> -u admin -p password","ad","WinRM shell")
tool("samdump2","samdump2 <system> <sam>","ad","Extract Windows password hashes")
tool("chntpw","chntpw <SAM>","ad","Windows password reset")

# ── TUNNEL ──
tool("proxychains","proxychains <command>","tunnel","Force apps through proxy")
tool("socat","socat TCP-LISTEN:8080,fork TCP:<target>:80","tunnel","Multipurpose relay")
tool("ncat","ncat -lvp 8080","tunnel","Netcat with SSL")
tool("iodine","iodine -d <server>","tunnel","DNS tunnel")
tool("redsocks","redsocks","tunnel","Transparent redirector")

# ── MITM ──
tool("mitmproxy","mitmproxy","mitm","Intercepting proxy")
tool("ettercap","ettercap -T -M arp:remote /<gateway>// /<target>//","mitm","ARP poisoning suite")
tool("sslstrip","sslstrip","mitm","SSL stripping")
tool("sslscan","sslscan <target>","mitm","SSL/TLS scanner")
tool("sslyze","sslyze <target>","mitm","SSL/TLS config analyzer")

# ── TRAFFIC ──
tool("tcpdump","tcpdump -i any -n","traffic","Packet analyzer")
tool("tshark","tshark -i any","traffic","Wireshark CLI tool")
tool("ngrep","ngrep -d any","traffic","Network grep")

# ── REVERSE ──
tool("radare2","r2 <binary>","reverse","Reverse engineering framework")
tool("gdb","gdb <binary>","reverse","GNU debugger")
tool("nasm","nasm -f elf64 <file>.asm","reverse","Netwide assembler")
tool("binwalk","binwalk <file>","reverse","Firmware analysis")
tool("foremost","foremost -i <file>","reverse","File carving")
tool("exiv2","exiv2 <file>","reverse","Image metadata tool")

# ── MISC ──
tool("arping","arping <target>","misc","ARP ping")
tool("windows-binaries","windows-binaries","misc","Windows binary collection")
tool("webshells","webshells","misc","Web shell collection")
tool("laudanum","laudanum","misc","Web shell injection kit")

CATS = [
    ("RECON",    [n for n,v in TOOLS.items() if v["cat"]=="recon"]),
    ("WEB",      [n for n,v in TOOLS.items() if v["cat"]=="web"]),
    ("EXPLOIT",  [n for n,v in TOOLS.items() if v["cat"]=="exploit"]),
    ("PASSWORD", [n for n,v in TOOLS.items() if v["cat"]=="password"]),
    ("WIRELESS", [n for n,v in TOOLS.items() if v["cat"]=="wireless"]),
    ("AD/WIN",   [n for n,v in TOOLS.items() if v["cat"]=="ad"]),
    ("TUNNEL",   [n for n,v in TOOLS.items() if v["cat"]=="tunnel"]),
    ("MITM",     [n for n,v in TOOLS.items() if v["cat"]=="mitm"]),
    ("TRAFFIC",  [n for n,v in TOOLS.items() if v["cat"]=="traffic"]),
    ("REVERSE",  [n for n,v in TOOLS.items() if v["cat"]=="reverse"]),
    ("MISC",     [n for n,v in TOOLS.items() if v["cat"]=="misc"]),
]

CHAINS = {
    "scan":     ("Quick vulnerability scan",                 ["nmap", "gobuster", "nikto"]),
    "recon":    ("Full reconnaissance",                      ["theharvester","dnsrecon","nmap","masscan","enum4linux","netexec"]),
    "web":      ("Web application attack",                   ["whatweb","nikto","wpscan","dirb","gobuster","ffuf","sqlmap"]),
    "exploit":  ("Exploitation chain",                       ["searchsploit","nmap","hydra"]),
    "brute":    ("Brute force (ssh ftp http mysql smb)",     []),
    "osint":    ("OSINT gathering",                          ["theharvester","dnsrecon","dnsenum","fierce","amass","cewl"]),
    "ad":       ("Active Directory",                         ["enum4linux","netexec","smbmap","responder"]),
    "wireless": ("Wireless attacks",                         ["airmon","airodump","aireplay","aircrack","wifite","reaver"]),
    "password": ("Password cracking",                        ["hashid","hashcat","john","crunch","cewl"]),
    "sql":      ("SQL injection",                            ["sqlmap"]),
    "full":     ("Full attack chain (recon+web+exploit+brute)",[]),
}

def run_chain(name, target):
    chain = CHAINS.get(name)
    if not chain: return
    logo()
    box_start(f"{name.upper()}  │ {chain[0]}  │ {S(target,G)}")
    start = datetime.now()
    for tool_name in chain[1]:
        if tool_name in TOOLS:
            cmd = TOOLS[tool_name]["cmd"].replace("<target>",target).replace("<domain>",target).replace("<url>",target)
            run(cmd, f"Running {tool_name} on {target}")
        print()
    if name == "brute":
        for svc in ["ssh","ftp","http-post-form","mysql","smb"]:
            run(f"hydra -l root -P /usr/share/wordlists/rockyou.txt.gz {target} {svc}", f"Brute forcing {svc}")
            print()
    if name == "full":
        for sub in ["recon","web","exploit","brute"]:
            run_chain(sub, target)
    elapsed = datetime.now() - start
    box_end()
    log("+", f"Chain '{name}' completed in {elapsed}")
    box_end()

def do_list():
    logo()
    box_start("TOOLS DATABASE", sep=True)
    for cat_name, tools in CATS:
        if not tools: continue
        box_line(f" {S(cat_name)}", R)
        for tn in tools:
            info = TOOLS[tn]
            desc = info["desc"][:30]
            box_line(f"  {tn:22}{D}{desc}{X}")
        box_line(f"{D}{'─'*BW}{X}", pad=False)
    box_start("ATTACK CHAINS", sep=True)
    for n, (d, _) in CHAINS.items():
        box_line(f"  {S(n + ':')}  {d}")
    box_end()

def do_help():
    logo()
    box_start("NEFERAX — Dark Security Framework", sep=True)
    box_line(f"{D}Usage:  {C}nefereax <command> [options] <target>{X}", D)
    box_line("")
    box_line(f"{S('ATTACK CHAINS:')}", R)
    for n, (d, _) in CHAINS.items():
        box_line(f"  {S(n):14}{d}")
    box_line("")
    box_line(f"{S('COMMANDS:')}", R)
    for c_, d_ in [("list","List all tools"),("search <q>","Search tools"),("info <t>","Tool details"),("menu","Interactive TUI"),("version","Show version")]:
        box_line(f"  {S(c_):14}{d_}")
    box_line("")
    box_line(f"{S('EXAMPLES:')}", R)
    for c_, d_ in [("nefereax scan 10.10.10.1","Quick scan"),("nefereax full 192.168.1.0/24","Full chain"),("nefereax info nmap","Tool info"),("nefereax search sql","Search tools")]:
        box_line(f"  {D}{c_:30}{X}  {d_}")
    box_end()

def do_version():
    logo()
    box_start(f"Nefereax v{V}  |  Dark Security Framework")
    box_line(f"  {D}{len(TOOLS)} tools  |  {len(CHAINS)} attack chains{X}")
    box_end()

def do_search(q):
    found = [(n, v) for n, v in TOOLS.items()
             if q in n.lower() or q in v["desc"].lower() or q in v["cmd"].lower()]
    logo()
    box_start(f"SEARCH RESULTS  {D}for '{q}'{X}")
    if found:
        for n, v in sorted(found):
            box_line(f"  {S(n):25}{D}{v['desc'][:30]}{X}")
    else:
        box_line(f"  {Y}No tools match '{q}'{X}")
    box_end()

def do_info(name):
    logo()
    if name in TOOLS:
        box_start(f"TOOL: {name}")
        box_line(f"  {D}Category: {TOOLS[name]['cat']}{X}")
        box_line(f"  {D}Usage:     {C}{TOOLS[name]['cmd']}{X}")
        box_line(f"  {D}About:     {TOOLS[name]['desc']}{X}")
    elif name in CHAINS:
        box_start(f"CHAIN: {name}")
        box_line(f"  {CHAINS[name][0]}")
        box_line(f"  {D}nefereax {name} <target>{X}")
    else:
        box_start(f"Unknown: {name}")
    box_end()

def do_unknown(cmd):
    logo()
    box_start(f"{Y}Unknown command: {cmd}{X}")
    box_line(f"  {D}Run 'nefereax --help' for usage{X}")
    box_end()

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h","--help","help"):
        do_help(); return 0

    cmd = sys.argv[1]
    if cmd == "version": do_version(); return 0
    if cmd == "menu": os.execv("/usr/bin/hackingtool", ["hackingtool"])
    if cmd == "list": do_list(); return 0

    if cmd == "search":
        if len(sys.argv) < 3:
            logo(); log("-", "Usage: nefereax search <query>"); return 1
        do_search(" ".join(sys.argv[2:]).lower()); return 0

    if cmd == "info":
        if len(sys.argv) < 3:
            logo(); log("-", "Usage: nefereax info <tool>"); return 1
        do_info(" ".join(sys.argv[2:]).lower()); return 0

    if cmd in CHAINS:
        if len(sys.argv) < 3:
            logo(); log("-", f"Usage: nefereax {cmd} <target>"); return 1
        target = " ".join(sys.argv[2:])
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        run_chain(cmd, target); return 0

    if cmd in TOOLS:
        if len(sys.argv) < 3:
            logo()
            box_start("Usage")
            box_line(f"  {TOOLS[cmd]['cmd']}")
            box_end()
            return 1
        target = " ".join(sys.argv[2:])
        tcmd = TOOLS[cmd]["cmd"].replace("<target>",target).replace("<domain>",target).replace("<url>",target)
        logo()
        run(tcmd, f"{cmd} on {target}")
        return 0

    do_unknown(cmd)
    return 1

if __name__ == "__main__":
    sys.exit(main())
