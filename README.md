
# recon_automation_bot — Recon Automation Bot for Bug Bounty

A Python-based pipeline to automate reconnaissance for bug bounty:  
**Amass → Shodan → Nmap (Docker)** to collect intelligence, then summarize findings with **Google Gemini AI** and save a formatted report into **Google Docs** via **Make.com**.

---

## Project overview
**Name:** `recon_automation_bot`  
**Purpose:** Automate subdomain enumeration, service fingerprinting, port and SSL/TLS checks, then summarize findings into a human-readable report stored in Google Docs.  
**Core tools:** Python 3.11+, Amass, Shodan API, Nmap (via Docker), Make.com, Google Gemini AI.

---

## Table of contents
1. Prerequisites  
2. Quick start (commands)  
3. Project layout  
4. .env / Secrets example  
5. Core scripts (what they do + examples)  
6. Make.com flow (high level)  
7. Gemini prompt (recommended)  
8. Output format & naming  
9. Security, ethics & legal notice  
10. Contribution & license

---

## 1. Prerequisites
- Python 3.11+  
- Docker (for Nmap Docker image)  
- Amass installed and on PATH (`amass`)  
- Shodan API key  
- Make.com account capable of webhooks and HTTP modules  
- Access to Google Docs via the Google account used in Make.com  
- (Optional) Google Gemini API credentials accessible to Make.com  
- Basic CLI familiarity

---

## 2. Quick start

```bash
# create project and virtualenv
mkdir recon_automation_bot && cd recon_automation_bot
python -m venv recon_bot_env

# activate
# Windows (cmd)
recon_bot_env\Scripts\activate
# macOS / Linux
# source recon_bot_env/bin/activate

# install dependencies
pip install requests shodan pandas python-dotenv
# subprocess is part of stdlib; no install required

# example usage (after populating .env)
python amass_runner.py example.com
python shodan_scanner.py example.com_amass.txt
python nmap_runner.py example.com
# or a wrapper script that runs all steps and posts to Make.com webhook
```

---

## 3. Project layout (recommended)

```
recon_automation_bot/
├─ recon_bot_env/               # venv
├─ .env                         # API keys + config (gitignored)
├─ requirements.txt
├─ README.md
├─ amass_runner.py              # enumerate_subdomains(domain)
├─ shodan_scanner.py            # scan_with_shodan(subdomains)
├─ nmap_runner.py               # nmap_scan(domain) -> ports & ssl outputs
├─ summarizer.py                # prepare files + send to Make.com webhook
├─ utils/
│  ├─ fileio.py
│  └─ dns_utils.py
└─ outputs/
   ├─ example.com_amass.txt
   ├─ example.com_shodan.json
   └─ example.com_nmap_ports_YYYYMMDDT....txt
```

---

## 4. `.env` / Secrets example
Create `.env` (add it to `.gitignore`):

```
SHODAN_API_KEY=your_shodan_key_here
MAKE_WEBHOOK_URL=https://hook.make.com/your_webhook_id
AMASS_PATH=amass              # or full path if not in PATH
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json  # if needed locally
```

Load values in Python via `python-dotenv`:
```python
from dotenv import load_dotenv
import os
load_dotenv()
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")
```

---

## 5. Core scripts — summary & examples

### `amass_runner.py` — `enumerate_subdomains(domain: str) -> List[str]`
Runs Amass in passive mode via `subprocess` and returns deduplicated subdomains.

```python
# amass_runner.py (outline)
import subprocess
from typing import List

def enumerate_subdomains(domain: str) -> List[str]:
    cmd = ["amass", "enum", "-passive", "-d", domain]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        subdomains = sorted(set(line.strip() for line in result.stdout.splitlines() if line.strip()))
        return subdomains
    except subprocess.CalledProcessError as e:
        print("Amass failed:", e.stderr)
        return []
```

**Output:** `outputs/<domain>_amass.txt` (one subdomain per line)

---

### `shodan_scanner.py` — `scan_with_shodan(subdomains: List[str]) -> dict`
Resolves each subdomain to an IP and uses the Shodan API to fetch host data (ports, banners, org, os). Returns a dictionary keyed by subdomain.

```python
# shodan_scanner.py (outline)
from shodan import Shodan
import socket

def resolve(hostname: str) -> str:
    try:
        return socket.gethostbyname(hostname)
    except Exception:
        return ""

def scan_with_shodan(subdomains: List[str], api_key: str) -> dict:
    api = Shodan(api_key)
    results = {}
    for sd in subdomains:
        ip = resolve(sd)
        if not ip:
            results[sd] = {"error": "dns_failed"}
            continue
        try:
            host = api.host(ip)
            results[sd] = {
                "ip": ip,
                "ports": host.get("ports", []),
                "services": host.get("data", []),
                "org": host.get("org"),
                "os": host.get("os")
            }
        except Exception as e:
            results[sd] = {"error": str(e)}
    return results
```

---

### `nmap_runner.py` — `nmap_docker_scan(domain: str) -> dict`
Performs two Nmap scans using a Dockerized Nmap image and saves outputs to the `outputs/` folder.

```python
# nmap_runner.py (outline)
import subprocess
import datetime
import os

def nmap_docker_scan(domain: str, out_dir="outputs"):
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    os.makedirs(out_dir, exist_ok=True)
    ports_file = os.path.join(out_dir, f"{domain}_nmap_ports_{timestamp}.txt")
    ssl_file = os.path.join(out_dir, f"{domain}_nmap_ssl_{timestamp}.txt")

    port_cmd = [
        "docker", "run", "--rm",
        "instrumentisto/nmap",
        "-sV", "-p1-1000", domain
    ]
    ssl_cmd = [
        "docker", "run", "--rm",
        "instrumentisto/nmap",
        "--script", "ssl-enum-ciphers", "-p", "443", domain
    ]

    with open(ports_file, "w", encoding="utf-8") as f:
        try:
            subprocess.run(port_cmd, stdout=f, stderr=subprocess.STDOUT, check=True, text=True)
        except subprocess.CalledProcessError:
            f.write("\n[nmap port scan failed]\n")

    with open(ssl_file, "w", encoding="utf-8") as f:
        try:
            subprocess.run(ssl_cmd, stdout=f, stderr=subprocess.STDOUT, check=True, text=True)
        except subprocess.CalledProcessError:
            f.write("\n[nmap ssl scan failed]\n")

    return {"ports": ports_file, "ssl": ssl_file}
```

---

## 6. Nmap (Docker) example (manual)
If you want to run Nmap locally with Docker (no Python):

```bash
docker run --rm instrumentisto/nmap -sV -p1-1000 example.com > outputs/example.com_ports.txt
docker run --rm instrumentisto/nmap --script ssl-enum-ciphers -p 443 example.com > outputs/example.com_ssl.txt
```

These commands write full Nmap output (services, versions, SSL ciphers) to text files.

---

## 7. Make.com flow (high level)
**Goal:** Accept up to three recon files via webhook → call Gemini API to summarize → convert Markdown → Google Docs.

Flow:
1. **Custom Webhook (Trigger)**  
   - Accepts 1–3 file uploads (.txt / .json).  
2. **HTTP / Google Gemini (Make.com HTTP module)**  
   - Send files and prompt to Gemini; receive structured Markdown summary.  
3. **Markdown → HTML**  
   - Convert Gemini's Markdown to HTML for rich formatting.  
4. **Google Docs – Create Document**  
   - Create a new Google Doc titled: `recon_<domain>_<YYYYMMDDTHHMMZ>` and paste the content.
5. **Optional: Notify**  
   - Slack/email with link to the created Doc.

---

## 8. Gemini prompt (recommended)
Use a structured prompt to instruct Gemini to parse input files and return Markdown. Example:

```
You are a security recon assistant. Inputs: up to three files (Amass, Shodan, Nmap).
For each file:
- Identify domain and timestamp (if available).
- List discovered subdomains.
- Summarize open ports and services (port, service, version).
- Highlight exposed admin interfaces, outdated services, or weak TLS configs.
- Extract certificate metadata (subject, issuer, expiration).
- Provide severity (Low/Med/High/Critical) for each critical finding and a one-line remediation.

Output: Markdown with sections:
# Target: <domain>
## Executive Summary
## Critical Findings
## Services & Ports
## Certificates
## Suggested Next Steps

Return only Markdown.
```

---

## 9. Output format & naming
Store outputs in `outputs/`:
- `<domain>_amass.txt`
- `<domain>_shodan.json`
- `<domain>_nmap_ports_<TIMESTAMP>.txt`
- `<domain>_nmap_ssl_<TIMESTAMP>.txt`

Google Doc title format:
```
recon_<domain>_<YYYY-MM-DDTHH:MM:SSZ>
```

---

## 10. Security, ethics & legal notice
- Only run recon against targets you have explicit permission to test (bug bounty program or written authorization). Unauthorized scanning may violate laws and platform terms.  
- Keep API keys and service-account credentials secret. Do not commit them to version control.  
- Sanitize reports before sharing publicly.

---

## 11. Contribution & license
- Contributions welcome via issues and pull requests.  
- Suggested license: MIT. Add a `LICENSE` file if you choose to use MIT.
