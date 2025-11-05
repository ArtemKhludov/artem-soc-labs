# MITRE ATT&CK Mapping - Case 001: RDP Brute Force

## Attack Chain Overview

```
Initial Access  Discovery  Lateral Movement  (Blocked)
    T1078         T1087         T1021
```


## Detailed Technique Mapping

### TA0001: Initial Access

#### T1078 - Valid Accounts
**Sub-technique:** T1078.002 - Domain Accounts

**Evidence:**
- Successful RDP login using `svc_backup` domain account
- Credentials obtained via brute force
- Authentication logged in Event ID 4624

**Detection:**
```
Event ID: 4624
Logon Type: 10 (RemoteInteractive)
Source IP: 185.220.101.45 (external)
```


#### T1110.001 - Brute Force: Password Guessing

**Evidence:**
- Multiple failed login attempts (Event ID 4625)
- Sequential username testing: administrator, admin, backup, svc_backup
- Attack completed in < 30 seconds

**Detection:**
```yaml
Failed Attempts: 4
Time Window: 12 seconds
Pattern: Dictionary attack
Success Rate: 25% (1/4)
```


### TA0006: Credential Access

#### T1110 - Brute Force

**Procedure:**
1. Target identification: RDP service (port 3389)
2. Username enumeration: Common admin accounts
3. Password spraying: Dictionary-based attack
4. Success: `svc_backup` with weak password

**SIEM Detection Rule:**
```sql
event_id=4625 
| stats count by source_ip, user 
| where count > 3 
| where time_span < 60s
```


### TA0007: Discovery

#### T1087.002 - Account Discovery: Domain Account

**Evidence:**
- Command executed: `net user /domain`
- Purpose: Enumerate domain users
- Timestamp: 14:23:45 UTC

**Detection:**
```
Process: net.exe
CommandLine: net user /domain
Parent Process: cmd.exe
User: svc_backup
```

**Prevention:**
- Service accounts should not have domain enumeration rights
- EDR should alert on `net.exe` execution from RDP sessions


#### T1083 - File and Directory Discovery

**Evidence:**
- `whoami` command execution
- System reconnaissance
- Process: cmd.exe


### TA0008: Lateral Movement

#### T1021.001 - Remote Desktop Protocol

**Evidence:**
- RDP session established
- Source: 185.220.101.45 (external)
- Destination: WS-FINANCE-01
- Protocol: TCP/3389

**Network Flow:**
```
185.220.101.45:52341  203.0.113.50:3389 (RDP)
```


#### T1021.002 - SMB/Windows Admin Shares

**Evidence:**
- SMB connection attempt to Domain Controller
- Source: 192.168.10.55 (WS-FINANCE-01)
- Destination: 192.168.10.100:445
- Status: **BLOCKED by EDR**

**Detection:**
```
Event ID: 5156 (Windows Firewall)
Protocol: SMB
Action: Allowed (internal), but flagged by EDR
```


## Detection Coverage Matrix

| Technique | Coverage | Tool | Status |
|-----------|----------|------|--------|
| T1078 |  Full | SIEM, Windows Logs | Detected |
| T1110.001 |  Full | SIEM Alert | Detected |
| T1087.002 |  Full | EDR, Process Monitoring | Detected |
| T1021.001 |  Full | Network Logs | Detected |
| T1021.002 |  Full | EDR, Firewall | **BLOCKED** |


## Defensive Recommendations

### Per Technique:

**T1078 (Valid Accounts):**
-  Implement MFA on all RDP
-  Service account password rotation (90 days  30 days)
-  Monitor for off-hours logins

**T1110 (Brute Force):**
-  Rate limiting: 3 failed attempts = 5 min lockout
-  IP reputation checking
-  Honeypot accounts for early detection

**T1087 (Account Discovery):**
-  Restrict `net.exe` usage on endpoints
-  Remove domain user enumeration rights from service accounts
-  Alert on reconnaissance commands

**T1021 (Lateral Movement):**
-  Network segmentation (Finance dept isolated)
-  Disable SMBv1
-  Monitor for lateral movement patterns


## Threat Actor Profile

**TTP Similarity:**
- APT28 (Fancy Bear): Known for RDP brute force
- Wizard Spider: Uses similar discovery techniques

**Attribution Confidence:** Low (common TTP)


## MITRE Navigator Layer

```json
{
  "name": "Case-001_RDP_BruteForce",
  "versions": {
    "attack": "13",
    "navigator": "4.9.1"
  },
  "techniques": [
    {
      "techniqueID": "T1078",
      "color": "#ff6666",
      "comment": "Service account compromised"
    },
    {
      "techniqueID": "T1110.001",
      "color": "#ff6666",
      "comment": "Brute force successful"
    },
    {
      "techniqueID": "T1087.002",
      "color": "#ffaa00",
      "comment": "Domain user enumeration"
    },
    {
      "techniqueID": "T1021.001",
      "color": "#ff6666",
      "comment": "RDP session established"
    },
    {
      "techniqueID": "T1021.002",
      "color": "#66ff66",
      "comment": "SMB blocked by EDR"
    }
  ]
}
```


## References

- [MITRE ATT&CK - T1078](https://attack.mitre.org/techniques/T1078/)
- [MITRE ATT&CK - T1110](https://attack.mitre.org/techniques/T1110/)
- [NSA Cybersecurity Advisory: RDP Security](https://media.defense.gov/2020/Jun/09/2002313081/-1/-1/0/CSI-SECURE-RDP-CONNECTIONS.PDF)


_Mapped by: Artem Khludov, SOC Analyst_  
_Date: 2025-10-08_

