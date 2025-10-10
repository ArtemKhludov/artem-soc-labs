# Professional Experience Summary

## Current Position

**SOC Analyst (L1/L2)**  
**EnergyLogic AI**  
**Duration:** July 2025 – Present (4 months)  
**Location:** Remote


## Role Overview

I work as a Security Operations Center analyst responsible for threat detection, incident response, and security monitoring for critical energy infrastructure systems. I handle 20-30 security incidents per week, ranging from phishing attempts to sophisticated intrusion attempts.


## Key Responsibilities

### 1. Security Monitoring & Threat Detection
- I monitor SIEM platform (Splunk) for security events across 500+ endpoints
- I analyze EDR telemetry (CrowdStrike Falcon) for suspicious activities
- I triage and investigate 20-30 security alerts daily
- I identify false positives vs true security incidents (95% accuracy rate)

### 2. Incident Response
- I lead incident response for HIGH and CRITICAL severity alerts
- I execute incident response playbooks following NIST framework
- I contain and remediate security incidents within SLA (average 22 min response time)
- I coordinate with IT teams for host isolation and remediation
- I document incidents and create detailed triage reports

### 3. Threat Intelligence & Detection Engineering
- I develop and tune SIEM detection rules (Splunk SPL)
- I map security incidents to MITRE ATT&CK framework
- I create custom detection rules for emerging threats
- I maintain IOC database and threat intelligence feeds
- I integrate threat intelligence into security operations

### 4. Vulnerability Management
- I analyze vulnerability scan results (Nessus, Qualys)
- I prioritize vulnerabilities based on risk and exploitability
- I work with system owners on remediation timelines
- I track vulnerability remediation progress


## Major Incidents Handled

### Case 001: RDP Brute Force Attack (October 2025)
- **Severity:** HIGH
- **Impact:** Compromised service account, attempted lateral movement
- **Response:** Detected in real-time, contained within 15 minutes
- **Outcome:** No data exfiltration, account secured, MFA implemented
- **Documentation:** Full case study in `/cases/Case-001_RDP-BruteForce/`

### Case 002: Phishing with Encoded PowerShell (September 2025)
- **Severity:** CRITICAL
- **Impact:** Malicious macro execution, attempted C2 communication
- **Response:** EDR blocked payload, host isolated within 5 minutes
- **Outcome:** Zero data loss, created detection rule now in production
- **Documentation:** `/cases/Case-002_PowerShell-EncodedCommand/`

### Additional Incidents (Jul-Oct 2025)
- **Total incidents handled:** ~380
- **False positive rate:** <5%
- **Average detection time:** <2 minutes
- **Average response time:** 22 minutes
- **Escalation rate:** 12% (to L2/L3)


## Technical Skills Developed

### SIEM & Security Platforms
- **Splunk:** SPL query development, dashboard creation, alert tuning
- **CrowdStrike Falcon:** Threat hunting, IOC searching, host containment
- **Windows Event Logs:** Deep analysis of Security, Sysmon, PowerShell logs
- **Firewall logs:** Palo Alto, Fortinet log analysis

### Threat Detection
- I created 15+ custom detection rules (95%+ accuracy)
- I map incidents to MITRE ATT&CK framework
- I perform behavioral analysis and anomaly detection
- I correlate logs across multiple data sources

### Incident Response
- I apply NIST IR Framework
- I conduct digital forensics investigations
- I analyze memory and disk artifacts
- I reconstruct attack timelines
- I collect and preserve evidence

### Scripting & Automation
- **Python:** I developed EDR log parser, triage automation scripts (5 tools)
- **PowerShell:** I write Windows forensics and AD query scripts
- **Bash:** I create log analysis and automation scripts
- **YAML:** I develop detection rules


## Projects & Achievements

### 1. EDR Triage Automation Tool
- **Tech Stack:** Python, JSON parsing
- **Impact:** Reduced triage time from 15 min to 2 min (87% improvement)
- **Usage:** Used daily by SOC team
- **Code:** `soc-operations/edr_triage.py`

### 2. IR Automation Framework
- **Tech Stack:** Python, SIEM integration
- **Features:** Automated log analysis, IOC extraction, MITRE mapping
- **Impact:** Saved 5 hours per week of manual work
- **Code:** `incident-response/triage_script.py`

### 3. CVE Risk Assessment Tool
- **Tech Stack:** Python, NVD API integration
- **Features:** Automated CVE lookup, risk scoring, report generation
- **Impact:** Vulnerability prioritization improved by 40%
- **Code:** `vulnerability-management/cve_parser.py`

### 4. Custom Detection Rules
- **Platform:** Splunk, Elastic SIEM
- **Rules Created:** 15+ production-ready detection rules
- **False Positive Rate:** <2%
- **Coverage:** RDP attacks, PowerShell abuse, lateral movement, exfiltration


## Training & Certifications

### Completed Training
- **TryHackMe:** SOC Level 1 Path (Completed)
- **HackTheBox:** 15+ machines solved
- **BlueTeam Labs Online:** IR and Detection challenges
- **SANS Webinars:** Threat Hunting, Detection Engineering

### In Progress
- **CompTIA Security+** (Expected: November 2025)
- **BTL1** (Blue Team Level 1) (Expected: December 2025)

### Planned
- **CEH** (Certified Ethical Hacker) - Q1 2026
- **OSCP** (Offensive Security Certified Professional) - Q2-Q3 2026


## Key Metrics (Jul-Oct 2025)

| Metric | Value |
|--------|-------|
| **Total Alerts Reviewed** | ~4,500 |
| **Incidents Handled** | 380 |
| **Critical Incidents** | 12 |
| **High Severity** | 89 |
| **False Positive Rate** | 4.8% |
| **Average Detection Time** | 1.8 minutes |
| **Average Response Time** | 22 minutes |
| **SLA Compliance** | 98.5% |
| **Escalation Rate** | 12% |
| **Detection Rules Created** | 15 |
| **Automation Scripts** | 7 |


## Professional Development

### Daily Activities
- I monitor security events during 8-hour shifts
- I triage and investigate alerts
- I update incident documentation
- I research threat intelligence

### Weekly
- I participate in team meetings and knowledge sharing
- I tune detection rules
- I optimize security tools
- I practice in personal lab (TryHackMe, HackTheBox)

### Monthly
- I participate in incident retrospectives
- I work on training and certification goals
- I update portfolio and documentation
- I join purple team exercises


## Work Environment

**Team Structure:**
- SOC Team: 8 analysts (3 shifts, 24/7 coverage)
- Reporting to: SOC Manager
- Collaboration: IT Operations, Security Engineering, Threat Intel

**Tech Stack:**
- SIEM: Splunk Enterprise
- EDR: CrowdStrike Falcon
- Firewall: Palo Alto Networks
- Ticketing: ServiceNow
- Communication: Slack, PagerDuty
- Documentation: Confluence

**Work Model:** Fully remote  
**Shift:** Day shift (9 AM - 6 PM local time)  
**On-call:** Rotating on-call schedule (1 week per month)


## Career Goals

### Short-term (6-12 months)
- Obtain CompTIA Security+ certification
- Complete BTL1 certification
- Transition to SOC L2/Senior Analyst role
- Develop advanced threat hunting skills

### Medium-term (1-2 years)
- Achieve CEH and OSCP certifications
- Move into Detection Engineering or Threat Intelligence role
- Lead purple team exercises
- Mentor junior SOC analysts

### Long-term (3-5 years)
- SOC Team Lead or Security Architect
- Specialize in Threat Hunting or Red Team operations
- Contribute to open-source security tools
- Speaking at security conferences


## References

Available upon request.

**Last Updated:** October 2025  
**Portfolio:** https://github.com/ArtemKhludov/artem-soc-labs  
**Contact:** artemKhludov@gmail.com  
**LinkedIn:** linkedin.com/in/artem-khludov

