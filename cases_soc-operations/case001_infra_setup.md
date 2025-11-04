# Case 001: Infrastructure Setup

## Objective
Set up a working environment for SOC analysis by installing necessary tools, virtual machines, and analysis environment.

## Tasks
- [x] Install Python 3.8+
- [x] Configure virtual machine (Kali Linux / Ubuntu)
- [x] Install basic tools (Wireshark, Nmap, tcpdump)
- [x] Configure SIEM (optional: Splunk Free, ELK Stack)
- [x] Create first Python script for log analysis

## Tools
- **VirtualBox / VMware** - for virtual machines
- **Python** - scripting language
- **Wireshark** - network traffic analysis
- **Nmap** - network scanning

## Workflow

### 1. Python Installation
```bash
python3 --version
pip3 install --upgrade pip
```

I verified Python 3.9.6 was installed and upgraded pip to the latest version.

### 2. Virtual Machine Setup
- Downloaded Kali Linux ISO
- Created VM with 4GB RAM, 2 CPU cores, 40GB HDD
- Installed guest additions

I chose Kali Linux as it comes with most security tools pre-installed, which saves time during setup.

### 3. Basic Tools Installation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install tools
sudo apt install wireshark nmap tcpdump python3-pip -y
```

All tools installed successfully. I configured Wireshark to capture packets without root privileges by adding my user to the wireshark group.

### 4. First Script
Created `edr_triage.py` to analyze EDR logs for suspicious events. The script parses JSON logs and identifies potential security incidents based on keyword matching.

## Results
- Environment configured successfully
- All tools installed and tested
- First script working and tested with sample logs

## Notes
**Observations and useful commands:**

- Wireshark requires root privileges for packet capture, but can be configured to run without root by adding user to wireshark group
- Nmap requires sudo for SYN scans by default
- Python virtual environments should be created for each project to isolate dependencies
- VirtualBox guest additions improve VM performance and enable features like shared folders

## References
- [Kali Linux Download](https://www.kali.org/get-kali/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Wireshark User Guide](https://www.wireshark.org/docs/)

---
**Date:** October 8, 2024  
**Status:** Completed

