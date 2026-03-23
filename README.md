[🔥 ─ Modular DDoS Testing Toolkit.md](https://github.com/user-attachments/files/26172263/Modular.DDoS.Testing.Toolkit.md)
<!-- HEADER ANIMADO -->
<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:000000,30:1a0000,60:660000,100:cc0000&height=220&section=header&text=devilZERO&fontSize=78&fontColor=ffffff&fontAlignY=40&desc=Modular%20DDoS%20Testing%20Toolkit&descSize=20&descAlignY=65&descColor=ff4444&animation=fadeIn&stroke=cc0000&strokeWidth=2" width="100%"/>
</div>

<!-- TYPING ANIMATION -->
<div align="center">
<img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&size=22&duration=3000&pause=800&color=FF4444&center=true&vCenter=true&width=620&lines=Modular+DDoS+Testing+Toolkit+%F0%9F%92%A5;Layer4+%26+Layer7+Attack+Vectors;Amplification+Attacks+%7C+Proxy+Support;For+Authorized+Security+Assessments+Only;%24+run+devilzero+%E2%80%94+krypthane" alt="Typing SVG"/>
</div>

<br/>

<!-- BADGES DE ESTADO Y TECNOLOGÍA -->
<div align="center">

[![Version](https://img.shields.io/badge/version-1.0.0-06b6d4?style=for-the-badge&labelColor=0d0000)](https://github.com/wavegxz-design/devilZERO/releases)
&nbsp;
[![Python](https://img.shields.io/badge/Python-3.8+-4ade80?style=for-the-badge&logo=python&logoColor=white&labelColor=0d0000)](https://www.python.org/)
&nbsp;
[![License](https://img.shields.io/badge/License-MIT-8b5cf6?style=for-the-badge&labelColor=0d0000)](LICENSE)
&nbsp;
[![Platform](https://img.shields.io/badge/Kali%20·%20Parrot%20·%20Ubuntu-f97316?style=for-the-badge&logo=linux&logoColor=white&labelColor=0d0000)](https://github.com/wavegxz-design/devilZERO)
&nbsp;
[![Stars](https://img.shields.io/github/stars/wavegxz-design/devilZERO?style=for-the-badge&color=ff4444&labelColor=0d0000)](https://github.com/wavegxz-design/devilZERO/stargazers)

</div>

<br/>

---

## 🔥 `devilZERO` ─ Modular DDoS Testing Toolkit

> **`devilZERO`** is a cutting-edge, modular DDoS testing toolkit engineered for **authorized security assessments** and **ethical penetration testing**. It provides a robust suite of attack vectors to simulate Distributed Denial of Service scenarios across various layers, helping security professionals identify and mitigate vulnerabilities in their infrastructure.

**Key Capabilities:**
*   **Layer 4 Attacks:** Comprehensive support for TCP, UDP, SYN, ICMP, Minecraft, VSE, and TS3/FiveM floods.
*   **Layer 7 Attacks:** Advanced HTTP/HTTPS floods, including Cloudflare bypass (CFB/CFBUAM), session-based requests, dynamic host randomization, and WordPress XMLRPC amplification.
*   **Amplification Vectors:** Exploits DNS, NTP, RDP, CLDAP, MEM, CHAR, and ARD for powerful reflection attacks.
*   **Utilities & Analytics:** Real-time packet/byte counters, IP geolocation, proxy management, and color-coded terminal output for enhanced situational awareness.

**⚠️ IMPORTANT: Ethical Use Only**
This tool is strictly intended for **authorized security assessments** and **educational purposes**. Unauthorized use against systems you do not own or have explicit permission to test is illegal and unethical. The author (krypthane) is not responsible for any misuse or damage caused by this software.

---

## ✨ Features at a Glance

<div align="center">

| Category | Attack Vector | Description | Key Options |
|:----------|:---------------|:------------|:-------------|
| 🎯 **Layer 4** | `TCP Flood` | Connect flood with random payloads | `target`, `port`, `threads` |
| | `UDP Flood` | High-rate UDP packet injection | `target`, `port`, `threads`, `size` |
| | `SYN Flood` | Raw TCP SYN packet storm (requires root) | `target`, `port`, `threads` |
| | `ICMP Flood` | Ping flood (requires root) | `target`, `threads` |
| | `Minecraft` | Server ping spam with handshake | `target`, `port` |
| | `MCBOT` | Automated bot login and chat flood | `target`, `port`, `bots` |
| | `VSE / TS3 / FiveM` | Game server query attacks | `target`, `port` |
| 🌐 **Layer 7** | `GET / POST` | Configurable HTTP/HTTPS request floods | `target`, `threads`, `method` |
| | `CFB / CFBUAM` | Cloudflare-resistant methods | `target`, `threads` |
| | `BYPASS` | Session-based requests | `target`, `threads` |
| | `STRESS` | High-payload JSON POST | `target`, `threads`, `data` |
| | `SLOW` | Slow-rate connection keep-alive (Slowloris) | `target`, `threads` |
| | `DYN` | Dynamic host header randomization | `target`, `threads` |
| | `TOR` | .onion via tor2web gateways | `target`, `threads` |
| | `XMLRPC` | WordPress pingback amplification | `target`, `threads` |
| | `BOT` | Crawler emulation (robots.txt + sitemap) | `target`, `threads` |
| 💥 **Amplification** | `DNS / NTP / RDP` | Reflection attacks with reflectors | `target`, `reflector_list` |
| | `CLDAP / MEM / CHAR` | Legacy protocol amplification | `target`, `reflector_list` |
| | `ARD` | Apple Remote Desktop flood | `target`, `reflector_list` |
| 🛠️ **Utilities** | `Ping` | ICMP reachability check | `host` |
| | `IP Info` | Geolocation and ISP lookup | `ip_address` |
| | `Proxy Management` | Auto-download and validation from public lists | `fetch`, `validate` |
| 📊 **Stats** | `PPS / BPS` | Real-time packet/byte counters | `N/A` |
| | `Color Output` | Severity-coded terminal logs | `N/A` |

</div>

---

## 📦 Installation

`devilZERO` is designed for ease of deployment across various Linux distributions, with a strong recommendation for security-focused environments like Kali Linux, Parrot OS, or Ubuntu.

### Prerequisites
*   **Python 3.8+**
*   **`pip`** (Python package installer)
*   **(Optional) Docker:** For containerized deployment and isolation.

### Method 1: Virtual Environment (Recommended for Kali Linux)
Using a Python virtual environment is the most secure and recommended approach, especially on systems with `externally-managed-environment` policies (e.g., Kali Linux). This prevents conflicts with system-wide Python packages.

```bash
# Clone the repository
git clone https://github.com/wavegxz-design/devilZERO.git
cd devilZERO

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run devilZERO
devilzero
```

### Method 2: Docker (Containerized Deployment)
For maximum isolation and portability, `devilZERO` can be run within a Docker container. This ensures all dependencies are self-contained and avoids system-level modifications.

```bash
# Clone the repository
git clone https://github.com/wavegxz-design/devilZERO.git
cd devilZERO

# Build the Docker image
docker build -t devilzero .

# Run devilZERO in a container
docker run -it devilzero
```

---

## 🚀 Usage

`devilZERO` offers both an interactive menu and direct CLI execution for its modules. After installation, simply run the `devilzero` command.

### Interactive Menu
```bash
┌─[krypthane@redteam]─[~]
└──╼ $ devilzero

  ██████╗ ███████╗██╗   ██╗██╗     ██╗     ███████╗ ██████╗ ██████╗ 
  ██╔══██╗██╔════╝██║   ██║██║     ██║     ██╔════╝██╔═══██╗██╔══██╗
  ██║  ██║█████╗  ██║   ██║██║     ██║     █████╗  ██║   ██║██████╔╝
  ██║  ██║██╔══╝  ██║   ██║██║     ██║     ██╔══╝  ██║   ██║██╔══██╗
  ██████╔╝███████╗╚██████╔╝███████╗███████╗███████╗╚██████╔╝██║  ██║
  ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝

  devilZERO v1.0.0 — Modular DDoS Testing Toolkit
  by krypthane (wavegxz-design) — Ethical Hacking Only

  1. Layer 4 Attacks
  2. Layer 7 Attacks
  3. Amplification Attacks
  4. Utilities
  5. Proxy Management
  6. Exit

  Select an option: _
```

### CLI Execution (Example: SYN Flood)
```bash
┌─[krypthane@redteam]─[~]
└──╼ $ devilzero layer4 syn --target 192.168.1.1 --port 80 --threads 100

  [INFO] Starting SYN Flood on 192.168.1.1:80 with 100 threads...
  [ATTACK] Sending SYN packet to 192.168.1.1:80 (Thread 1)
  [ATTACK] Sending SYN packet to 192.168.1.1:80 (Thread 2)
  ...
  [STATS] PPS: 1250 | BPS: 60000
  [STATUS] Attack in progress. Press Ctrl+C to stop.
```

---

## 🗺️ Roadmap

*   **Advanced Evasion Techniques:** Implement more sophisticated methods to bypass WAFs and anti-DDoS solutions.
*   **Distributed Architecture:** Support for multi-node attacks and botnet simulation (for authorized testing).
*   **Reporting & Logging:** Enhanced logging capabilities and automated report generation.
*   **GUI Interface:** Development of an optional graphical user interface for easier interaction.

---

## 👤 Author & Contact

`devilZERO` is developed and maintained by **krypthane** (wavegxz-design), a Red Team Operator and Open Source Developer focused on ethical security research and tool development.

<div align="center">

[![Portfolio](https://img.shields.io/badge/🌐_Portfolio-krypthane.workernova.workers.dev-cc0000?style=for-the-badge&labelColor=0d0000)](https://krypthane.workernova.workers.dev)
&nbsp;
[![GitHub](https://img.shields.io/badge/GitHub-wavegxz--design-ff4444?style=for-the-badge&logo=github&logoColor=white&labelColor=1a0000)](https://github.com/wavegxz-design)
&nbsp;
[![Telegram](https://img.shields.io/badge/Telegram-Skrylakk-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white&labelColor=0d0000)](https://t.me/Skrylakk)
&nbsp;
[![Email](https://img.shields.io/badge/ProtonMail-Workernova-6D4AFF?style=for-the-badge&logo=protonmail&logoColor=white&labelColor=0d0000)](mailto:Workernova@proton.me)

</div>

---

<!-- FOOTER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:cc0000,50:660000,100:000000&height=130&section=footer&text=ethical+hacking+only&fontSize=18&fontColor=ff4444&fontAlignY=65&animation=fadeIn" width="100%" alt="Ethical Hacking Only"/>
