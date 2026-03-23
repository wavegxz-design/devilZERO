<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,40:dc2626,100:7c3aed&height=200&section=header&text=devilZERO&fontSize=80&fontColor=ffffff&fontAlignY=40&desc=DDoS%20Testing%20Toolkit&descSize=22&descAlignY=62&descColor=94a3b8&animation=fadeIn" width="100%"/>

<br>

[![Version](https://img.shields.io/badge/version-1.0.0-06b6d4?style=for-the-badge&labelColor=0d1117)](https://github.com/wavegxz-design/devilZERO/releases)
[![Python](https://img.shields.io/badge/Python-3.8+-4ade80?style=for-the-badge&logo=python&logoColor=white&labelColor=0d1117)](https://www.python.org/)
[![License](https://img.shields.io/badge/MIT-8b5cf6?style=for-the-badge&labelColor=0d1117)](LICENSE)
[![Platform](https://img.shields.io/badge/Kali%20·%20Parrot%20·%20Ubuntu-f97316?style=for-the-badge&logo=linux&logoColor=white&labelColor=0d1117)](https://github.com/wavegxz-design/devilZERO)

<br>

**Modular DDoS testing suite for authorized security assessments.**  
Layer4, Layer7, Amplification attacks — all in one powerful toolkit.

<br>

[Features](#-features) · [Install](#-install) · [Usage](#-usage) · [Modules](#-modules) · [Roadmap](#-roadmap) · [Author](#-author)

</div>

---

## 🔥 What is devilZERO?

**devilZERO** is a comprehensive DDoS testing toolkit designed for penetration testers and security researchers. It implements multiple attack vectors across:

- **Layer4** (TCP, UDP, SYN, Minecraft, VSE, etc.)
- **Layer7** (HTTP/HTTPS floods with various bypass methods)
- **Amplification** (DNS, NTP, RDP, CLDAP, etc.)

The tool features a clean CLI interface, an interactive menu, proxy support, real‑time packet/byte counters, and a modular architecture. It is intended **only for authorized security assessments** and educational purposes.

**⚠️ IMPORTANT**: Unauthorized use is illegal. The author is not responsible for any misuse or damage.

---

## ✨ Features

| Category | Feature | Description |
|----------|---------|-------------|
| 🎯 **Layer4** | TCP Flood | Connect flood with random payloads |
| | UDP Flood | High‑rate UDP packet injection |
| | SYN Flood | Raw TCP SYN packet storm (requires root) |
| | ICMP Flood | Ping flood (requires root) |
| | Minecraft | Server ping spam with handshake |
| | MCBOT | Automated bot login and chat flood |
| | VSE / TS3 / FiveM | Game server query attacks |
| 🌐 **Layer7** | GET / POST | Configurable HTTP/HTTPS request floods |
| | CFB / CFBUAM | Cloudflare‑resistant methods |
| | BYPASS | Session‑based requests |
| | STRESS | High‑payload JSON POST |
| | SLOW | Slow‑rate connection keep‑alive (Slowloris) |
| | DYN | Dynamic host header randomization |
| | TOR | .onion via tor2web gateways |
| | XMLRPC | WordPress pingback amplification |
| | BOT | Crawler emulation (robots.txt + sitemap) |
| | STOMP | Captcha challenge flooding |
| 💥 **Amplification** | DNS / NTP / RDP | Reflection attacks with reflectors |
| | CLDAP / MEM / CHAR | Legacy protocol amplification |
| | ARD | Apple Remote Desktop flood |
| 🛠️ **Utilities** | Ping | ICMP reachability check |
| | IP Info | Geolocation and ISP lookup |
| | Proxy Management | Auto‑download and validation from public lists |
| 📊 **Stats** | PPS / BPS | Real‑time packet/byte counters |
| | Color Output | Severity‑coded terminal logs |

---

## 📦 Install

### Prerequisites
- Python 3.8+
- pip
- (Optional) Docker

### Method 1: Virtual Environment (Recommended for Kali)

Kali Linux (and some other distros) enforce the `externally-managed-environment` policy. Using a virtual environment is the safest way.

```bash
git clone https://github.com/wavegxz-design/devilZERO.git
cd devilZERO
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
devilzero
