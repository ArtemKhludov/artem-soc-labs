# Artem Khludov - SOC Analyst Portfolio

**Security Operations Center Analyst | Threat Detection | Incident Response**

---

## Professional Summary

SOC Analyst with **4 months of hands-on experience** at **EnergyLogic AI** (July-October 2025), specializing in threat detection, incident response, and security automation. Successfully handled 380+ security incidents with 98.5% SLA compliance and <5% false positive rate.

**Core Expertise:**
- Threat Detection & Analysis - SIEM/EDR monitoring, alert triage, IOC hunting
- Incident Response - NIST framework, containment, eradication, forensics
- Security Automation - Python scripting for SOC operations
- SIEM Engineering - Splunk SPL, detection rule development
- MITRE ATT&CK - Threat mapping and adversary emulation
- Vulnerability Management - CVE analysis, risk assessment

## Professional Experience

### SOC Analyst (L1/L2)
**EnergyLogic AI** | July 2025  Present (4 months) | Remote

**Key Achievements:**
- Responded to 380+ security incidents (avg response time: 22 min)
- Developed 15+ custom detection rules with 95%+ accuracy
- Created 7 automation tools reducing triage time by 87%
- Handled 12 critical incidents including RDP brute force and phishing attacks
- Maintained 98.5% SLA compliance and <5% false positive rate

**Daily Responsibilities:**
- Monitor SIEM (Splunk) and EDR (CrowdStrike) for 500+ endpoints
- Triage and investigate 20-30 security alerts daily
- Execute incident response playbooks following NIST framework
- Develop and tune detection rules mapped to MITRE ATT&CK
- Document incidents and create detailed triage reports

[Full Experience Summary](resume/experience_summary.md)

## Case Studies & Incident Reports

### Real-World Incidents Handled

| Case ID | Title | Date | Severity | Response Time | Status |
|---------|-------|------|----------|---------------|--------|
| **[Case-001](cases/Case-001_RDP-BruteForce/)** | RDP Brute Force Attack | Oct 2025 | HIGH | 15 min |  Resolved |
| **[Case-002](cases/Case-002_PowerShell-EncodedCommand/)** | Malicious PowerShell Execution | Sep 2025 | CRITICAL | 20 min |  Resolved |

**Each case includes:**
- Detailed triage notes with timeline
- MITRE ATT&CK technique mapping
- Incident response playbook
- IOCs and detection rules
- Lessons learned and recommendations

## Security Tools & Projects

### SOC Automation Suite

#### SOC Operations ([soc-operations/](soc-operations/))

**EDR Log Triage Tool**
- Automated analysis of EDR events (CrowdStrike, SentinelOne)
- JSON log parsing and suspicious activity detection
- Triage time reduced from 15 min to ~2 min
- Tech: Python, JSON parsing, pattern matching

**[Case 002: Triage Automation](soc-operations/case002_triage_basics/)**
- Real-time log analysis with multiple detection engines
- Automated IOC extraction and threat intelligence enrichment
- Tech: Python, threat intelligence APIs

#### Vulnerability Management ([vulnerability-management/](vulnerability-management/))

**CVE Analysis Toolkit**
- Automated CVE data retrieval from NVD database
- CVSS-based risk scoring and prioritization
- Vulnerability assessment report generation
- Tech: Python, NVD API, risk assessment algorithms

**Network Security Scanner**
- Nmap automation for infrastructure scanning
- Service enumeration and vulnerability detection
- Tech: Python, python-nmap, network analysis

#### Incident Response ([incident-response/](incident-response/))

**IR Automation Framework**
- NIST-based incident response playbook implementation
- Automated log analysis (auth.log, syslog, Windows Events)
- Brute force detection and IOC identification
- Tech: Python, log parsing, SIEM integration

**MITRE ATT&CK Mapping Tool**
- Automatic technique identification from incident data
- Attack chain visualization
- Detection coverage analysis

#### Red Team Operations ([redteam-operations/](redteam-operations/))

**Reconnaissance Suite**
- Nmap automation for network enumeration
- Directory brute force tool (DirBuster simulation)
- Adversary simulation for purple team exercises
- Tech: Python, threading, HTTP analysis

Note: All offensive tools used only in authorized lab environments

## Detection Rules & Playbooks

### Custom Detection Rules ([detections/](detections/))

**Production-Ready SIEM Rules:**
- RDP Brute Force Detection (Splunk SPL, KQL, Sigma)
- Encoded PowerShell Execution (Multi-platform)
- Lateral Movement via SMB
- Suspicious Process Injection
- Data Exfiltration Patterns

**Platforms Supported:**
- Splunk Enterprise
- Elastic SIEM
- Microsoft Sentinel
- CrowdStrike Falcon

---

### Incident Response Playbooks ([playbooks/](playbooks/))

**Operational Playbooks:**
- RDP Brute Force Response (30-60 min playbook)
- Malware Investigation & Remediation
- Phishing Email Analysis
- Data Breach Response
- Ransomware Incident Handling

All playbooks follow NIST SP 800-61 framework

## Key Metrics (Jul-Oct 2025)

| Metric | Achievement |
|--------|-------------|
| **Security Incidents Handled** | 380+ |
| **Average Response Time** | 22 minutes |
| **SLA Compliance** | 98.5% |
| **False Positive Rate** | <5% |
| **Detection Rules Created** | 15+ |
| **Automation Tools Developed** | 7 |
| **Critical Incidents Resolved** | 12 |
| **Triage Time Reduction** | 87% (via automation) |

## Technical Skills

### Security Operations
- SIEM Platforms: Splunk (SPL), Elastic (KQL), Microsoft Sentinel
- EDR Solutions: CrowdStrike Falcon, SentinelOne
- Log Analysis: Windows Event Logs, Sysmon, Linux system logs
- Network Security: Wireshark, tcpdump, Zeek, Suricata
- Threat Intelligence: MISP, OpenCTI, VirusTotal, AbuseIPDB

### Scripting & Automation
- Python - SOC automation, log parsing, API integration
- PowerShell - Windows forensics, Active Directory queries
- Bash - Linux system analysis, log analysis
- YAML/JSON - Detection rule development, data parsing

### Frameworks & Standards
- MITRE ATT&CK - Threat mapping and detection engineering
- NIST Cybersecurity Framework - Incident response and operations
- OWASP Top 10 - Web application security
- Kill Chain - Threat modeling and analysis

### Tools & Technologies
- Platforms: Linux, Windows, macOS
- Version Control: Git, GitHub
- Ticketing: ServiceNow, Jira
- Collaboration: Confluence, Slack, Microsoft Teams

## Certifications & Training

### Current Focus
- CompTIA Security+ (In Progress - Expected Nov 2025)
- BTL1 (Blue Team Level 1) (In Progress - Expected Dec 2025)

### Completed Training
- TryHackMe: SOC Level 1 Path
- HackTheBox: 15+ machines solved
- BlueTeam Labs Online: IR scenarios completed
- SANS Webcasts: Threat Hunting, Detection Engineering

### Planned Certifications
- CEH (Certified Ethical Hacker) - Q1 2026
- OSCP (Offensive Security Certified Professional) - Q2-Q3 2026

## External Profiles & Research

### Professional Platforms
- **GitHub:** [@ArtemKhludov](https://github.com/ArtemKhludov)
- **LinkedIn:** [linkedin.com/in/artem-khludov](https://linkedin.com/in/artem-khludov)
- **TryHackMe:** [artemsoc](https://tryhackme.com/p/artemsoc)

### Security Research Projects ([research-projects/](research-projects/))
- TryHackMe challenge write-ups
- HackTheBox machine solutions
- Network traffic analysis (PCAP files)
- Threat hunting methodologies

---

## Portfolio Structure

```
artem-soc-labs/

 cases_cybersecurity/            # Real incident case studies
    Case-001_RDP-BruteForce/
    Case-002_PowerShell-EncodedCommand/
    Case-003_Splunk-Integration-Failure/
    Case-004_Cloudflare-SpamForms/
    Case-005_Autopilot-Intune-Control/

 cases_soc-operations/           # SOC automation and notes
    edr_triage.py
    edr_triage_sample.json
    case001_infra_setup.md
    case002_triage_basics/
      logs_sample.json
      triage_notes.md
      triage_parser_v2.py
    notes_summary.md

 docs/                           # Guides and references
    achievements.md
    professional_development.md
    splunk_cheatsheet.md
    splunk_management_guide.md
    tools_list.md

 research-projects/              # CTF and research (kept with .gitkeep)
    hackthebox_results/
    tryhackme_notes/
    wireshark_sessions/

 resume/
    experience_summary.md

 requirements.txt
 SETUP.md
 README.md
 triage_parser.py
```

---

## Quick Start

### Clone Repository
```bash
git clone https://github.com/ArtemKhludov/artem-soc-labs.git
cd artem-soc-labs
```

### Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run EDR Triage Tool
```bash
cd cases_soc-operations
python edr_triage.py
```

```

 **[Full Setup Guide](SETUP.md)**

---

## Contact

**Email:** artemKhludov@gmail.com  
**Location:** Remote  
**Availability:** Open to SOC Analyst (L2/L3) and Detection Engineering roles

## Portfolio Notes

This portfolio demonstrates real-world SOC operations experience. All tools, case studies, and detection rules are from actual incident response work at EnergyLogic AI.

Focus areas: production-ready tools, real incident case studies, MITRE ATT&CK-mapped detection rules, SOC automation.

## Legal Disclaimer

All security tools and techniques documented in this portfolio are used only in authorized environments: personal lab setups, authorized penetration testing engagements, employer-sanctioned SOC operations, CTF platforms (TryHackMe, HackTheBox).

Unauthorized access to computer systems is illegal.

## License

Portfolio for demonstration purposes. Code samples provided as-is under MIT License.

**Last Updated:** October 2025
