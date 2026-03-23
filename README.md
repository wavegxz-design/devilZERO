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

**devilZERO** is a comprehensive DDoS testing toolkit designed for penetration testers and security researchers. It implements multiple attack vectors across Layer4 (TCP/UDP/SYN/Minecraft), Layer7 (HTTP/HTTPS floods), and amplification techniques (DNS/NTP/RDP). The tool features a clean CLI interface with interactive menu, proxy support, and real-time statistics.

**⚠️ IMPORTANT**: This tool is for educational purposes and authorized testing only. Unauthorized use is illegal.

---

## ✨ Features

| Category | Feature | Description |
|----------|---------|-------------|
| 🎯 **Layer4** | TCP Flood | Connect flood with random payloads |
| | UDP Flood | High‑rate UDP packet injection |
| | SYN Flood | Raw TCP SYN packet storm |
| | Minecraft | Server ping spam with handshake |
| | VSE / TS3 / FiveM | Game server query attacks |
| | MCBOT | Automated bot login/chat flood |
| 🌐 **Layer7** | HTTP GET/POST | Configurable request floods |
| | CFB / CFBUAM | Cloudflare bypass methods |
| | Slowloris | Keep‑alive connection exhaustion |
| | XML‑RPC | WordPress pingback amplification |
| | BOT | Search‑engine crawler simulation |
| 💥 **Amplification** | DNS / NTP / RDP | Reflection attacks with reflectors |
| | CLDAP / MEM / CHAR | Legacy protocol amplification |
| 🛠️ **Utilities** | Ping | ICMP reachability check |
| | IP Info | Geolocation and ISP lookup |
| | Proxy Management | Auto‑download and validation |
| 📊 **Stats** | PPS / BPS | Real‑time packet/byte counters |
| | Color Output | Severity‑coded terminal logs |

---

## ⚡ Install

### From GitHub
```bash
git clone https://github.com/wavegxz-design/devilZERO.git
cd devilZERO
pip install -e .
