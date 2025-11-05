# Incident Response Playbook: RDP Brute Force Attack

**Playbook ID:** IR-PB-001  
**Version:** 1.0  
**Last Updated:** 2025-10-08  
**Author:** Artem Khludov, SOC Analyst


## Playbook Overview

| Field | Value |
|-------|-------|
| **Incident Type** | RDP Brute Force / Account Compromise |
| **MITRE Tactic** | Initial Access (TA0001) |
| **Severity** | HIGH |
| **Estimated Time** | 30-60 minutes |
| **Required Tools** | SIEM, EDR, Firewall, Active Directory |


## Trigger Conditions

This playbook is activated when:

- [ ] 5+ failed RDP login attempts from single IP within 60 seconds
- [ ] Successful RDP login after multiple failed attempts
- [ ] RDP connection from non-standard geolocation
- [ ] SIEM alert: "RDP_BRUTE_FORCE_DETECTED"


## Response Workflow

### Phase 1: Detection & Triage (0-5 minutes)

#### Step 1: Validate the Alert

```bash
# Check SIEM for RDP events
index=windows EventCode=4625 OR EventCode=4624
| where dest_port=3389
| stats count by src_ip, user, _time
| where count > 3
```

**Decision Point:**
-  **True Positive:** Multiple failures + external IP  Proceed to Phase 2
-  **False Positive:** Internal IP + valid user  Close alert


#### Step 2: Identify Affected Systems

**Information to Gather:**
- [ ] Target hostname/IP
- [ ] Compromised username (if any)
- [ ] Attacker source IP
- [ ] Timestamp of first/last attempt
- [ ] Success status (breach or just attempts?)

**Tools:**
```powershell
# Query Windows Security Logs
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    ID=4625,4624
    StartTime=(Get-Date).AddHours(-1)
} | Where-Object {$_.Properties[19].Value -eq 3389}
```


### Phase 2: Containment (5-15 minutes)

#### Step 3: Block Attacker IP

**Firewall:**
```bash
# Block on perimeter firewall
fw-cli add rule src_ip=185.220.101.45 action=drop

# Verify block
fw-cli show blocked-ips | grep 185.220.101.45
```

**EDR:**
```bash
# Add to EDR block list
edr-cli block-ip --ip 185.220.101.45 --reason "RDP brute force"
```


#### Step 4: Disable Compromised Account (if breached)

**Active Directory:**
```powershell
# Disable user account
Disable-ADAccount -Identity "svc_backup"

# Force logout all sessions
quser /server:WS-FINANCE-01
logoff <session_id> /server:WS-FINANCE-01

# Confirm account disabled
Get-ADUser -Identity "svc_backup" | Select-Object Enabled
```


#### Step 5: Isolate Affected Host

**Network Isolation:**
```bash
# Method 1: VLAN quarantine
switch> vlan quarantine
switch> switchport access vlan 999
switch> interface GigabitEthernet0/1
switch> shutdown

# Method 2: EDR isolation
edr-cli isolate-host --hostname WS-FINANCE-01
```

**Verification:**
```bash
ping WS-FINANCE-01  # Should fail
```


### Phase 3: Eradication (15-30 minutes)

#### Step 6: Terminate Malicious Sessions

```powershell
# List active RDP sessions
qwinsta /server:WS-FINANCE-01

# Kill malicious session
rwinsta <session_id> /server:WS-FINANCE-01

# Verify termination
qwinsta /server:WS-FINANCE-01
```


#### Step 7: Hunt for Persistence Mechanisms

**Check for:**
- [ ] Scheduled tasks
- [ ] Registry run keys
- [ ] New user accounts
- [ ] Backdoor services

```powershell
# Scheduled tasks
Get-ScheduledTask | Where-Object {$_.Author -like "*svc_backup*"}

# Registry persistence
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run

# New accounts
Get-LocalUser | Where-Object {$_.Created -gt (Get-Date).AddHours(-2)}

# Suspicious services
Get-Service | Where-Object {$_.DisplayName -like "*remote*"}
```


#### Step 8: Scan for Malware

```bash
# EDR full scan
edr-cli scan --host WS-FINANCE-01 --type full

# Windows Defender
Start-MpScan -ScanType FullScan

# Check results
Get-MpThreatDetection | Where-Object {$_.InitialDetectionTime -gt (Get-Date).AddHours(-2)}
```


### Phase 4: Recovery (30-45 minutes)

#### Step 9: Password Reset

```powershell
# Force password change
Set-ADUser -Identity "svc_backup" -ChangePasswordAtLogon $true
Set-ADAccountPassword -Identity "svc_backup" -Reset

# Notify user/IT team
Send-MailMessage -To "it-team@company.com" -Subject "Password Reset Required" -Body "..."
```


#### Step 10: Restore Network Access

**Prerequisites:**
- [ ] Malware scan clean
- [ ] Password changed
- [ ] No suspicious activity in last 30 min

```bash
# Remove from quarantine VLAN
switch> no vlan 999
switch> vlan 10
switch> switchport access vlan 10

# Un-isolate from EDR
edr-cli unisolate-host --hostname WS-FINANCE-01
```


#### Step 11: Re-enable Account (if needed)

```powershell
Enable-ADAccount -Identity "svc_backup"
Get-ADUser -Identity "svc_backup" | Select-Object Enabled
```


### Phase 5: Post-Incident (45-60 minutes)

#### Step 12: Evidence Collection

**Collect:**
- [ ] Windows Event Logs (Security, System, Application)
- [ ] Firewall logs
- [ ] EDR telemetry
- [ ] Network flow logs

```powershell
# Export Security logs
wevtutil epl Security C:\Evidence\Security_$(Get-Date -F yyyy-MM-dd).evtx

# Copy to forensics share
Copy-Item C:\Evidence\* \\forensics-server\cases\case-001\
```


#### Step 13: Update Threat Intelligence

```bash
# Add IOC to threat feed
ioc-cli add --type ip --value 185.220.101.45 --severity high --source case-001

# Share with community
misp-cli add-event --type "RDP Brute Force" --ioc 185.220.101.45
```


#### Step 14: Create Incident Report

**Required Sections:**
- Executive summary
- Timeline
- IOCs
- Root cause analysis
- Recommendations

**Template:** `incident_report_template.md`


### Phase 6: Lessons Learned (Post-Incident)

#### Step 15: Implement Preventive Measures

**Short-term:**
- [ ] Enable MFA on RDP
- [ ] Implement rate limiting (3 attempts = 5 min lockout)
- [ ] IP whitelist for RDP access

**Long-term:**
- [ ] Deploy honeypot RDP servers
- [ ] Network segmentation
- [ ] Zero Trust architecture


#### Step 16: Update Detection Rules

```yaml
# Enhanced SIEM rule
rule: rdp_brute_force_v2
severity: high
conditions:
  - event_id: 4625
  - port: 3389
  - failed_attempts: >= 3
  - time_window: 60 seconds
  - geo_location: outside_US  # NEW
  - source_reputation: < 50   # NEW
action: 
  - alert_soc
  - auto_block_ip             # NEW
  - isolate_host              # NEW
```


## Decision Tree

```
RDP Alert
    ├── External IP?
    │   ├── Yes  High Priority
    │   └── No  Check user
    │       ├── Service Account?  High Priority
    │       └── Regular User?  Medium Priority
    │
    ├── Failed Attempts > 5?
    │   ├── Yes  Auto-block IP
    │   └── No  Monitor
    │
    └── Successful Login After Failures?
        ├── Yes  CRITICAL - Execute full playbook
        └── No  Medium - Block IP + Monitor
```


## Escalation Path

| Severity | Notify | Timeline |
|----------|--------|----------|
| **CRITICAL** | SOC Manager, CISO, IT Director | Immediate |
| **HIGH** | SOC Lead, Security Engineer | 15 minutes |
| **MEDIUM** | SOC Analyst (L2) | 30 minutes |


## Tools Reference

| Tool | Purpose | Command |
|------|---------|---------|
| SIEM | Log analysis | `splunk search "EventCode=4625"` |
| EDR | Endpoint isolation | `edr-cli isolate-host` |
| AD | Account management | `Disable-ADAccount` |
| Firewall | IP blocking | `fw-cli add rule` |

## Response Checklist

- Alert validated
- Systems identified
- IP blocked
- Account disabled
- Host isolated
- Sessions terminated
- Persistence checked
- Malware scan complete
- Password reset
- Access restored
- Evidence collected
- IOCs shared
- Report created
- Prevention implemented

## References

- NIST SP 800-61: Computer Security Incident Handling Guide
- SANS Incident Handler's Handbook
- Microsoft: Detecting RDP Brute Force Attacks

Used in ~20 incidents. Avg response time ~20 min. Applied to Case-001 on 2025-10-08 (response: 15 min).

