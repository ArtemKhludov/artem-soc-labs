# Setup Guide

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/ArtemKhludov/artem-soc-labs.git
cd artem-soc-labs
```

### 2. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python --version
pip list
```

## Tool Usage

### SOC Operations

**EDR Log Triage Tool:**
```bash
cd soc-operations
python edr_triage.py
```

Analyzes EDR events from `edr_triage_sample.json`.

### Vulnerability Management

**Network Security Scanner:**
```bash
cd vulnerability-management
python nmap_scan_example.py 192.168.1.1 --all
```

Options: `--quick`, `--service`, `--vuln`, `--all`

**CVE Parser:**
```bash
python cve_parser.py CVE-2021-44228 -o report.json
```

Retrieves CVE data from NVD and assesses risk.

### Incident Response

**IR Triage Script:**
```bash
cd incident-response
python triage_script.py --log-dir logs -o triage_report.json
```

Analyzes auth.log and syslog for compromise indicators.

### Red Team Operations

**Nmap Reconnaissance:**
```bash
cd redteam-operations/recon_tools
python nmap_recon.py 192.168.1.1 --full
```

Options: `--stealth`, `--services`, `--os`, `--vuln`, `--full`

**Directory Brute Force:**
```bash
python dirbuster_sim.py http://example.com -t 10 -o report.json
```

Options: `-w` (wordlist), `-t` (threads), `-o` (output)

## Additional Tools

### Install Nmap

macOS: `brew install nmap`  
Ubuntu: `sudo apt install nmap`  
Windows: https://nmap.org/download.html

### Install Wireshark

macOS: `brew install --cask wireshark`  
Ubuntu: `sudo apt install wireshark`

## Troubleshooting

**ModuleNotFoundError:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Permission Denied (Nmap SYN scan):**
```bash
sudo python nmap_recon.py TARGET --stealth
```

**Demo Mode:**  
Scripts work in demo mode with synthetic data if dependencies (nmap, scapy) are not installed.

## Dependencies

- requests - HTTP requests (CVE parser)
- python-nmap - Nmap wrapper
- scapy - Network packet manipulation
- pandas/numpy - Data analysis
- colorama - Console colors
- pyyaml - YAML parsing

## Legal Notice

All tools for authorized testing only. Use on own systems or with explicit permission. Some scripts require sudo/admin privileges.

## References

- [Nmap Documentation](https://nmap.org/book/man.html)
- [NIST IR Framework](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [NVD Database](https://nvd.nist.gov/)

