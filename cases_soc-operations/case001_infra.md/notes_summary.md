# Week 1: Summary & Notes

## Main Topics
- SOC analyst environment setup
- First exposure to EDR logs
- Writing simple Python scripts for triage

## Key Takeaways

### 1. Infrastructure Setup
- Virtual machines are essential for safe testing environments
- Kali Linux includes most needed tools out of the box
- Python is the primary language for SOC automation tasks

I set up my analysis environment using Kali Linux in a virtual machine, which provides isolation and a comprehensive toolkit for security analysis.

### 2. EDR Log Analysis
- EDR logs contain endpoint events (process creation, network connections, file modifications)
- Filtering noise and identifying anomalies is critical
- Key indicators include: "suspicious", "alert", "malware", "ransomware"

During my first EDR log analysis, I learned to focus on process creation events and network connections, as these often reveal malicious activity patterns.

### 3. Scripting
- Simple Python scripts can automate routine tasks
- JSON is a common log format
- Regular expressions are useful for parsing

I created my first triage script to automate log analysis, which significantly reduced the time needed to review EDR events.

## Useful Commands

```bash
# Check network connections
netstat -tulnp

# View authentication logs
sudo tail -f /var/log/auth.log

# Quick analysis of suspicious processes
ps aux | grep -i suspicious

# Search logs
grep -i "failed" /var/log/syslog
```

## Problems and Solutions

| Problem | Solution |
|---------|----------|
| Python modules not installing | Use `python3 -m pip install` |
| Wireshark not capturing packets | Add user to `wireshark` group |
| JSON file not reading | Check encoding (UTF-8) |

I encountered several setup issues initially, but resolved them through documentation and troubleshooting. The most common issue was permission problems with network tools.

## Next Steps
- [ ] SIEM queries (Splunk SPL, KQL)
- [ ] Threat Intelligence feeds
- [ ] Incident Response Playbooks
- [ ] MITRE ATT&CK Framework

I plan to dive deeper into SIEM query languages and threat intelligence platforms to enhance my detection capabilities.

## Notes
**Observations and useful commands**

**Useful Resources:**
- https://attack.mitre.org/ - MITRE ATT&CK
- https://www.sans.org/blog/ - SANS Reading Room
- https://github.com/meirwah/awesome-incident-response

---
**Week:** 1  
**Date:** October 8, 2024  
**Time Spent:** ~10 hours

