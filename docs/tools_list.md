#  Security Tools Reference

Список инструментов для SOC, Blue Team и Red Team операций.


## Blue Team / SOC Tools

### SIEM & Log Analysis
| Tool | Purpose | Experience |
|------|---------|------------|
| **Splunk** | Enterprise SIEM |  |
| **ELK Stack** | Open-source log management |  |
| **Graylog** | Log aggregation & analysis |  |
| **Microsoft Sentinel** | Cloud-native SIEM |  |

### EDR / Endpoint Security
| Tool | Purpose | Experience |
|------|---------|------------|
| **CrowdStrike Falcon** | Next-gen AV & EDR |  |
| **SentinelOne** | AI-powered EDR |  |
| **Microsoft Defender for Endpoint** | Windows EDR |  |
| **Sysmon** | Windows activity monitoring |  |

### Network Monitoring
| Tool | Purpose | Experience |
|------|---------|------------|
| **Wireshark** | Packet analysis |  |
| **Zeek (Bro)** | Network security monitor |  |
| **Suricata** | IDS/IPS |  |
| **tcpdump** | Command-line packet capture |  |

### Threat Intelligence
| Tool | Purpose | Experience |
|------|---------|------------|
| **MISP** | Threat intel sharing platform |  |
| **AlienVault OTX** | Open threat exchange |  |
| **VirusTotal** | Malware & IOC check |  |
| **AbuseIPDB** | IP reputation check |  |


## Red Team / Offensive Tools

### Reconnaissance
| Tool | Purpose | Experience |
|------|---------|------------|
| **Nmap** | Network scanning |  |
| **Masscan** | Fast port scanner |  |
| **theHarvester** | OSINT email gathering |  |
| **Shodan** | Internet-wide device search |  |
| **Subfinder** | Subdomain enumeration |  |
| **Amass** | Attack surface mapping |  |

### Exploitation
| Tool | Purpose | Experience |
|------|---------|------------|
| **Metasploit** | Exploitation framework |  |
| **Burp Suite** | Web app pentesting |  |
| **SQLmap** | SQL injection automation |  |
| **Exploit-DB** | Public exploit database |  |

### Post-Exploitation
| Tool | Purpose | Experience |
|------|---------|------------|
| **Mimikatz** | Credential dumping |  |
| **BloodHound** | AD attack path mapping |  |
| **Impacket** | Network protocol toolkit |  |
| **CrackMapExec** | Post-ex Swiss army knife |  |
| **Empire/Starkiller** | PowerShell post-exploitation |  |

### C2 Frameworks
| Tool | Purpose | Experience |
|------|---------|------------|
| **Cobalt Strike** | Professional C2 (commercial) |  |
| **Sliver** | Open-source C2 |  |
| **Covenant** | .NET C2 framework |  |
| **Mythic** | Collaborative C2 |  |


## Vulnerability Assessment

| Tool | Purpose | Experience |
|------|---------|------------|
| **Nessus** | Vulnerability scanner |  |
| **OpenVAS** | Open-source vuln scanner |  |
| **Nuclei** | Fast vulnerability scanner |  |
| **Nikto** | Web server scanner |  |


## Forensics & Incident Response

| Tool | Purpose | Experience |
|------|---------|------------|
| **Volatility** | Memory forensics |  |
| **Autopsy** | Digital forensics platform |  |
| **FTK Imager** | Forensic imaging |  |
| **Velociraptor** | Endpoint visibility & forensics |  |
| **KAPE** | Triage & evidence collection |  |


##  Linux & System Tools

| Tool | Purpose | Experience |
|------|---------|------------|
| **Kali Linux** | Pentest distribution |  |
| **Parrot OS** | Security-focused OS |  |
| **Docker** | Containerization |  |
| **Git** | Version control |  |


##  Scripts & Automation

### My Custom Tools
- **edr_triage.py** - EDR log analysis automation
- **vuln_scanner.py** - Custom CVE parser (in development)
- **threat_hunter.py** - SIEM query automation (planned)
- **ioc_enrichment.sh** - Threat intel enrichment script (planned)

### Python Libraries Used
- `requests` - HTTP requests
- `json` - JSON parsing
- `re` - Regular expressions
- `subprocess` - System command execution
- `pandas` - Data analysis (for large logs)
- `scapy` - Packet manipulation


