# SOC Case-003: Alert Investigation - Suspicious Outbound Traffic

**Date:** November 14, 2025  
**Source:** SIEM Alert - Splunk  
**Analyst:** Artem Khludov  
**Tool:** Splunk, Wireshark, VirusTotal

## Initial Alert

Got an alert around 2:30 PM today from our SIEM about unusual outbound traffic from one of the workstations in accounting. The alert triggered because the machine was sending data to an IP that's not on our usual whitelist and the volume looked weird - around 400MB in 20 minutes.

## Investigation Steps

### 1. Checked the alert details

First thing I did was pull up the full alert in Splunk to see what we're dealing with:
- Source: WS-ACCT-07 (192.168.10.45)
- Destination IP: 185.220.102.8 (Russia)
- Port: 443 (HTTPS)
- Data transferred: ~400MB
- User logged in: jsmith (accounting manager)

This immediately felt off because jsmith doesn't usually move this much data, and definitely not to IPs outside the US.

### 2. Ran some queries

I checked if there were any similar patterns before:

```spl
index=firewall src_ip="192.168.10.45" 
| stats sum(bytes_out) as total_bytes by dest_ip
| where total_bytes > 100000000
```

Turns out this is the first time this workstation sent this much data anywhere. That's a red flag.

### 3. Looked at the destination IP

Ran the IP through VirusTotal and got 6 hits from different vendors flagging it as malicious. The IP was associated with data exfiltration campaigns in the past. Not good.

### 4. Checked what files were accessed

Pulled Windows logs from the EDR to see what jsmith was doing around that time:
- Accessed several Excel files from the shared finance folder
- Opened Outlook
- No PowerShell or cmd activity (which is good, means probably not ransomware)

### 5. Talked to the user

Called jsmith to ask if she noticed anything weird. She said she got an email this morning about updating the company expense tracker and clicked a link that opened what looked like our internal portal. She logged in with her credentials.

Bingo. Phishing.

## What I Found

So here's what happened:
1. jsmith clicked a phishing link
2. Entered her credentials on a fake page
3. The attacker used those creds to access her machine remotely (probably through VPN)
4. Started downloading files from the finance folder
5. Our firewall caught the large data transfer and triggered the alert

## Actions Taken

- Isolated WS-ACCT-07 from the network immediately
- Disabled jsmith's AD account
- Blocked 185.220.102.8 on the firewall
- Started collecting evidence (memory dump, disk image)
- Escalated to IR team
- Reset jsmith's password and set up MFA

## Timeline

| Time | Event |
|------|-------|
| 09:15 AM | Phishing email received |
| 09:23 AM | jsmith clicked link and entered credentials |
| 02:15 PM | Suspicious outbound connection started |
| 02:37 PM | SIEM alert triggered |
| 02:45 PM | I started investigation |
| 03:10 PM | Workstation isolated |
| 03:20 PM | Account disabled |

## Indicators of Compromise (IOCs)

- **Malicious IP:** 185.220.102.8
- **Phishing domain:** company-expense-update[.]tk (already taken down)
- **Compromised account:** jsmith
- **Affected host:** WS-ACCT-07

## Lessons Learned

This could've been way worse. We caught it because the attacker got greedy and tried to exfiltrate a lot of data quickly. If they had been patient and transferred files slowly over days, we might've missed it.

Need to:
- Push harder on phishing training for finance team
- Implement DLP rules to flag large file transfers
- Set up alerts for VPN logins from unusual geolocations

## MITRE ATT&CK Mapping

- **T1566.002** - Phishing: Spearphishing Link
- **T1078** - Valid Accounts
- **T1071.001** - Application Layer Protocol: Web Protocols
- **T1041** - Exfiltration Over C2 Channel

**Status:** Investigation complete, passed to IR for remediation  
**Severity:** HIGH  
**Estimated damage:** Potentially 15-20 financial documents compromised
