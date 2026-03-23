import socket
import ssl
import random
import warnings
from math import log2, trunc
from multiprocessing import RawValue
from re import compile
from struct import pack as data_pack
from typing import Tuple, List, Set, Any
from uuid import UUID, uuid4
from base64 import b64encode

import certifi
import requests
from cloudscraper import create_scraper
from icmplib import ping
from impacket.ImpactPacket import IP, TCP, UDP, Data, ICMP
from requests import Response, Session, get, cookies
from yarl import URL

from .utils import Colors

# Silence urllib3 warnings
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

__version__ = '1.0.0'

# Global counters
REQUESTS_SENT = None
BYTES_SEND = None

class Counter:
    def __init__(self, value=0):
        self._value = RawValue('i', value)
    def __iadd__(self, value):
        self._value.value += value
        return self
    def __int__(self):
        return self._value.value
    def set(self, value):
        self._value.value = value
        return self

# Initialize counters
REQUESTS_SENT = Counter()
BYTES_SEND = Counter()

# Get local IP
try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        LOCAL_IP = s.getsockname()[0]
except Exception:
    LOCAL_IP = '127.0.0.1'

# SSL context for HTTPS
SSL_CTX = ssl.create_default_context(cafile=certifi.where())
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# Tor2web gateways
tor2webs = [
    'onion.city', 'onion.cab', 'onion.direct', 'onion.sh', 'onion.link',
    'onion.ws', 'onion.pet', 'onion.rip', 'onion.plus', 'onion.top',
    'onion.si', 'onion.ly', 'onion.my', 'onion.sh', 'onion.lu', 'onion.casa',
    'onion.com.de', 'onion.foundation', 'onion.rodeo', 'onion.lat',
    'tor2web.org', 'tor2web.fi', 'tor2web.blutmagie.de', 'tor2web.to',
    'tor2web.io', 'tor2web.in', 'tor2web.it', 'tor2web.xyz', 'tor2web.su',
    'darknet.to', 's1.tor-gateways.de', 's2.tor-gateways.de', 's3.tor-gateways.de',
    's4.tor-gateways.de', 's5.tor-gateways.de'
]

# Search engine user agents (short version)
search_engine_agents = [
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Googlebot/2.1 (+http://www.googlebot.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0"
]

class Tools:
    IP = compile(r"(?:\d{1,3}\.){3}\d{1,3}")
    protocolRex = compile(r'"protocol":(\d+)')

    @staticmethod
    def humanbytes(i: int, binary: bool = False, precision: int = 2):
        MULTIPLES = ["B", "k{}B", "M{}B", "G{}B", "T{}B", "P{}B", "E{}B", "Z{}B", "Y{}B"]
        if i > 0:
            base = 1024 if binary else 1000
            multiple = trunc(log2(i) / log2(base))
            value = i / pow(base, multiple)
            suffix = MULTIPLES[multiple].format("i" if binary else "")
            return f"{value:.{precision}f} {suffix}"
        return "-- B"

    @staticmethod
    def humanformat(num: int, precision: int = 2):
        suffixes = ['', 'k', 'm', 'g', 't', 'p']
        if num > 999:
            obje = sum([abs(num / 1000.0 ** x) >= 1 for x in range(1, len(suffixes))])
            return f'{num / 1000.0 ** obje:.{precision}f}{suffixes[obje]}'
        return str(num)

    @staticmethod
    def sizeOfRequest(res: Response) -> int:
        size = len(res.request.method)
        size += len(res.request.url)
        size += len('\r\n'.join(f'{key}: {value}' for key, value in res.request.headers.items()))
        return size

    @staticmethod
    def send(sock: socket.socket, packet: bytes):
        global BYTES_SEND, REQUESTS_SENT
        if not sock.send(packet):
            return False
        BYTES_SEND += len(packet)
        REQUESTS_SENT += 1
        return True

    @staticmethod
    def sendto(sock, packet, target):
        global BYTES_SEND, REQUESTS_SENT
        if not sock.sendto(packet, target):
            return False
        BYTES_SEND += len(packet)
        REQUESTS_SENT += 1
        return True

    @staticmethod
    def dgb_solver(url, ua, pro=None):
        try:
            session = Session()
            if pro:
                session.proxies = pro
            headers = {
                "User-Agent": ua,
                "Accept": "text/html",
                "Accept-Language": "en-US",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "TE": "trailers",
                "DNT": "1"
            }
            session.get(url, headers=headers)
            headers = {
                "User-Agent": ua,
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Referer": url,
                "Sec-Fetch-Dest": "script",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "cross-site"
            }
            resp = session.post("https://check.ddos-guard.net/check.js", headers=headers)
            idss = None
            for key, value in resp.cookies.items():
                if key == '__ddg2':
                    idss = value
            if idss is None:
                return None
            headers = {
                "User-Agent": ua,
                "Accept": "image/webp,*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Cache-Control": "no-cache",
                "Referer": url,
                "Sec-Fetch-Dest": "script",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "cross-site"
            }
            session.get(f"{url}.well-known/ddos-guard/id/{idss}", headers=headers)
            return session
        except Exception:
            return None

    @staticmethod
    def safe_close(sock=None):
        if sock:
            sock.close()

class Minecraft:
    @staticmethod
    def varint(d: int) -> bytes:
        o = b''
        while True:
            b = d & 0x7F
            d >>= 7
            o += data_pack("B", b | (0x80 if d > 0 else 0))
            if d == 0:
                break
        return o

    @staticmethod
    def data(*payload: bytes) -> bytes:
        payload = b''.join(payload)
        return Minecraft.varint(len(payload)) + payload

    @staticmethod
    def short(integer: int) -> bytes:
        return data_pack('>H', integer)

    @staticmethod
    def long(integer: int) -> bytes:
        return data_pack('>q', integer)

    @staticmethod
    def handshake(target: Tuple[str, int], version: int, state: int) -> bytes:
        return Minecraft.data(Minecraft.varint(0x00),
                              Minecraft.varint(version),
                              Minecraft.data(target[0].encode()),
                              Minecraft.short(target[1]),
                              Minecraft.varint(state))

    @staticmethod
    def handshake_forwarded(target: Tuple[str, int], version: int, state: int, ip: str, uuid: UUID) -> bytes:
        return Minecraft.data(Minecraft.varint(0x00),
                              Minecraft.varint(version),
                              Minecraft.data(
                                  target[0].encode(),
                                  b"\x00",
                                  ip.encode(),
                                  b"\x00",
                                  uuid.hex.encode()
                              ),
                              Minecraft.short(target[1]),
                              Minecraft.varint(state))

    @staticmethod
    def login(protocol: int, username: str) -> bytes:
        if isinstance(username, str):
            username = username.encode()
        return Minecraft.data(Minecraft.varint(0x00 if protocol >= 391 else 0x01 if protocol >= 385 else 0x00),
                              Minecraft.data(username))

    @staticmethod
    def keepalive(protocol: int, num_id: int) -> bytes:
        return Minecraft.data(Minecraft.varint(0x0F if protocol >= 755 else 0x10 if protocol >= 712 else 0x0F if protocol >= 471 else 0x10 if protocol >= 464 else 0x0E if protocol >= 389 else 0x0C if protocol >= 386 else 0x0B if protocol >= 345 else 0x0A if protocol >= 343 else 0x0B if protocol >= 336 else 0x0C if protocol >= 318 else 0x0B if protocol >= 107 else 0x00),
                              Minecraft.long(num_id) if protocol >= 339 else Minecraft.varint(num_id))

    @staticmethod
    def chat(protocol: int, message: str) -> bytes:
        return Minecraft.data(Minecraft.varint(0x03 if protocol >= 755 else 0x03 if protocol >= 464 else 0x02 if protocol >= 389 else 0x01 if protocol >= 343 else 0x02 if protocol >= 336 else 0x03 if protocol >= 318 else 0x02 if protocol >= 107 else 0x01),
                              Minecraft.data(message.encode()))
