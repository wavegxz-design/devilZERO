from pathlib import Path
import json

__dir__ = Path(__file__).parent
DATA_DIR = __dir__ / 'data'

with open(DATA_DIR / 'config.json') as f:
    config = json.load(f)

MCBOT_NAME = config.get('MCBOT', 'MHDDoS_')
MINECRAFT_DEFAULT_PROTOCOL = config.get('MINECRAFT_DEFAULT_PROTOCOL', 47)
PROXY_PROVIDERS = config.get('proxy-providers', [])
