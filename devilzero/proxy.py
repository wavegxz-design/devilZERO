import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from random import choice
from typing import Set

from PyRoxy import Proxy, ProxyChecker, ProxyType, ProxyUtiles
from requests import get, exceptions

from .config import PROXY_PROVIDERS
from .utils import Colors

logger = logging.getLogger("devilZERO.proxy")

def handle_proxy_list(config, proxy_file: Path, proxy_type: int, target_url: str = None):
    """
    Download and validate proxies based on config.
    Returns a set of Proxy objects or None.
    """
    if proxy_type not in {4, 5, 1, 0, 6}:
        raise ValueError("Invalid proxy type. Must be 1,4,5,6,0")

    if proxy_type == 6:
        proxy_type = choice([4, 5, 1])

    if not proxy_file.exists():
        logger.warning("Proxy file does not exist. Downloading proxies...")
        proxy_file.parent.mkdir(parents=True, exist_ok=True)
        proxies = _download_proxies(proxy_type)
        if not proxies:
            logger.error("No proxies downloaded.")
            return None
        logger.info(f"Checking {len(proxies)} proxies (this may take a while)...")
        check_url = target_url or "http://httpbin.org/get"
        threads = 100
        proxies = ProxyChecker.checkAll(proxies, timeout=5, threads=threads, url=check_url)
        if not proxies:
            logger.error("Proxy check failed. No valid proxies found.")
            return None
        with open(proxy_file, 'w') as f:
            for proxy in proxies:
                f.write(str(proxy) + "\n")
        logger.info(f"Saved {len(proxies)} proxies to {proxy_file}")

    proxies = ProxyUtiles.readFromFile(proxy_file)
    if proxies:
        logger.info(f"Loaded {len(proxies)} proxies from {proxy_file}")
    else:
        logger.warning("Empty proxy file.")
    return proxies

def _download_proxies(proxy_type: int) -> Set[Proxy]:
    """
    Download proxies from providers defined in config.json.
    """
    providers = [p for p in PROXY_PROVIDERS if p["type"] == proxy_type or proxy_type == 0]
    if not providers:
        logger.warning("No proxy providers found for this type.")
        return set()

    all_proxies = set()
    with ThreadPoolExecutor(max_workers=len(providers)) as executor:
        futures = {executor.submit(_download_single, provider): provider for provider in providers}
        for future in as_completed(futures):
            try:
                proxies = future.result()
                all_proxies.update(proxies)
            except Exception as e:
                logger.error(f"Error downloading from {futures[future]['url']}: {e}")
    return all_proxies

def _download_single(provider) -> Set[Proxy]:
    url = provider["url"]
    timeout = provider["timeout"]
    proxy_type = ProxyType.stringToProxyType(str(provider["type"]))
    try:
        resp = get(url, timeout=timeout)
        lines = resp.text.splitlines()
        proxies = set()
        for line in lines:
            for proxy in ProxyUtiles.parseAllIPPort([line], proxy_type):
                proxies.add(proxy)
        return proxies
    except Exception as e:
        logger.error(f"Failed to download proxies from {url}: {e}")
        return set()
