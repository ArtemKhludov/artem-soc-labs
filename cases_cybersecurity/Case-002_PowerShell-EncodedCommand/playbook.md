# Incident Response Playbook: Malicious PowerShell Execution

**Playbook ID:** IR-PB-002  
**Version:** 1.0  
**Last Updated:** 2025-09-15  
**Author:** Artem Khludov, SOC Analyst


## Trigger Conditions

- [ ] EDR/SIEM alert: "Encoded PowerShell Execution"
- [ ] Parent process is Microsoft Office application
- [ ] PowerShell command contains `-enc` or `-encodedcommand`
- [ ] Suspicious network activity following PowerShell execution


## Quick Response Steps

### 1. Immediate Containment (0-5 min)

```bash
# Kill PowerShell process
Get-Process -Name powershell | Where-Object {$_.CommandLine -like "*-enc*"} | Stop-Process -Force

# Isolate host
edr-cli isolate-host --hostname <HOSTNAME>

# Block C2 IP on firewall
fw-cli block-ip --ip <ATTACKER_IP> --reason "Malicious PowerShell C2"
```

### 2. Analysis (5-15 min)

```powershell
# Decode Base64 command
$encoded = "SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQA..."
[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($encoded))

# Check process tree
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; ID=1} |
Where-Object {$_.Properties[4].Value -like "*powershell*"}

# Network connections
netstat -ano | findstr "ESTABLISHED" | findstr <PID>
```

### 3. Eradication (15-30 min)

- [ ] Remove malicious Word document
- [ ] Delete dropped files
- [ ] Check for persistence (scheduled tasks, registry)
- [ ] Full antivirus scan

### 4. Recovery (30-45 min)

- [ ] Un-isolate host (after clean scan)
- [ ] User password reset
- [ ] Security awareness training
- [ ] Monitor for 24 hours


## MITRE ATT&CK Mapping

- T1059.001 (PowerShell)
- T1027 (Obfuscation)
- T1204.002 (User Execution)
- T1105 (Ingress Tool Transfer)


**Average Response Time:** 18 minutes  
**Used in Case-002:** Response completed in 20 minutes 

