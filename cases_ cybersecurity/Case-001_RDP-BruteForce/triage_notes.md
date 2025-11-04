# Case 001: RDP Brute Force Attack

**Date:** October 8, 2025  
**Analyst:** Artem Khludov  
**Company:** EnergyLogic AI  
**Severity:** HIGH  
**Status:** Resolved


## Executive Summary

Detected and responded to an RDP brute force attack targeting Windows workstation WS-FINANCE-01. Attacker successfully compromised service account `svc_backup` after multiple failed attempts. Lateral movement detected via SMB. Account disabled, IP blocked, and affected host isolated within 15 minutes of detection.


## Timeline

| Time | Event | Status |
|------|-------|--------|
| 14:22:15 | Multiple RDP failed login attempts detected |  Alert |
| 14:22:27 | Successful RDP login (svc_backup) |  Breach |
| 14:23:05 | Suspicious cmd.exe execution |  Post-exploitation |
| 14:24:12 | Lateral movement via SMB |  Spreading |
| 14:35:00 | Account disabled, IP blocked |  Contained |
| 14:45:00 | Host isolated from network |  Remediated |


## Attack Chain Analysis

### 1. Initial Access (T1078)
- **Method:** RDP Brute Force
- **Target:** WS-FINANCE-01 (Finance Department)
- **Attacker IP:** 185.220.101.45 (external, known malicious)
- **Failed attempts:** 4 different usernames
- **Success:** `svc_backup` account (weak password detected)

### 2. Discovery (T1087)
- **Command:** `net user /domain`
- **Purpose:** Domain user enumeration
- **Data exfiltrated:** Domain user list

### 3. Lateral Movement (T1021)
- **Protocol:** SMB (port 445)
- **Target:** 192.168.10.100 (Domain Controller)
- **Status:** Connection established but blocked by EDR


## IOC (Indicators of Compromise)

### Network
- **Malicious IP:** `185.220.101.45`
  - Reputation: Known brute force bot
  - Geographic: Russia
  - Action: Blocked on firewall

### Compromised Account
- **Username:** `svc_backup`
- **Password:** Weak (dictionary word)
- **Action:** Disabled, password reset required

### Suspicious Processes
- `cmd.exe` spawned by rdpclip.exe (RDP clipboard)
- `net.exe` for domain reconnaissance


## Detection Logic

```yaml
# SIEM Rule: RDP Brute Force
rule: rdp_brute_force
severity: high
conditions:
  - event_id: 4625
  - port: 3389
  - failed_attempts: >= 3
  - time_window: 60 seconds
action: alert_soc, block_ip
```


## Response Actions

### Immediate (0-15 min)
- [x] Disabled compromised account `svc_backup`
- [x] Blocked attacker IP 185.220.101.45 on perimeter firewall
- [x] Isolated WS-FINANCE-01 from network

### Short-term (1 hour)
- [x] Forced password reset for all service accounts
- [x] Reviewed logs for other compromised hosts (none found)
- [x] Updated SIEM detection rules

### Long-term (24-48 hours)
- [x] Implemented RDP rate limiting
- [x] Deployed MFA for all RDP connections
- [x] Conducted security awareness training for IT team


## Root Cause

1. **Weak password** on service account (dictionary word)
2. **No MFA** on RDP connections
3. **No rate limiting** on authentication attempts
4. Service account had **excessive privileges** (domain user enum)

## Lessons Learned

**What worked:**
- I detected brute force in real-time using SIEM
- EDR blocked lateral movement attempt
- I contained the incident in 15 minutes

**What needs improvement:**
- Service account password policy needs strengthening
- RDP needs MFA implementation
- Need IP whitelist for administrative protocols

## Recommendations

1. **Immediate:**
   - Enable MFA on all RDP connections
   - Implement IP whitelisting for RDP
   - Audit all service account passwords

2. **Short-term:**
   - Deploy CrowdStrike EDR on remaining endpoints
   - Create honeypot RDP server for threat intelligence
   - Implement network segmentation for finance dept

3. **Long-term:**
   - Zero Trust architecture implementation
   - Privileged Access Management (PAM) solution
   - Regular purple team exercises


## MITRE ATT&CK Mapping

- **T1078:** Valid Accounts (Initial Access)
- **T1110.001:** Brute Force: Password Guessing
- **T1021.001:** Remote Desktop Protocol
- **T1087.002:** Domain Account Discovery
- **T1021.002:** SMB/Windows Admin Shares


## Supporting Evidence

- `logs_sample.json` - Raw event logs
- `detection_rule.yaml` - SIEM detection rule
- `playbook.md` - Response playbook used
- Network flow logs (stored in SIEM)
- EDR telemetry screenshots


**Reported to:** Security Manager, IT Director  
**Follow-up required:** 30-day review of MFA implementation  
**Status:** Closed - No data exfiltration detected

_Last updated: 2025-10-08_

