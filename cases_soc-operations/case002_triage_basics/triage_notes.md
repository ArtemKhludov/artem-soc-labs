# SOC Case-002: Triage Basics

**Date:** October 8, 2025  
**Source:** logs_sample.json  
**Analyst:** Artem Khludov  
**Tool:** Manual analysis  

## Detected Events
| # | Time | Action | User | Assessment |
|---|------|--------|------|------------|
| 1 | 09:15 | Successful login admin | admin | Normal |
| 2 | 09:20 | Failed login guest from external IP | guest | Suspicious |
| 3 | 09:22 | Access to system file /etc/shadow | guest | Dangerous |
| 4 | 09:25 | PowerShell execution | guest | Critical |

## Analysis

I analyzed the logs and identified several suspicious events. The guest account appears to be compromised. The attacker attempted to access password files and executed PowerShell, which is highly unusual for a guest account.

**Threat Level:** HIGH  
**Status:** Escalated to IR team

## MITRE ATT&CK Mapping
- **T1078** - Valid Accounts  
- **T1059** - Command and Scripting Interpreter  
