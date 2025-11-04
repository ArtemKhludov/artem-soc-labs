# MITRE ATT&CK Mapping - Case 005: Intune / Autopilot Policy Management

## Defense Chain Overview

```
Policy Enforcement  Defense Evasion Prevention
      TA0002            TA0005
```

## Detailed Technique Mapping

### TA0002: Execution

#### Policy Enforcement - System Configuration Management

**Implementation:**
- Centralized policy management through Microsoft Intune
- Automated policy enforcement on all devices
- Real-time policy synchronization and compliance checking
- Department-based policy assignment via dynamic groups

**Detection:**
```
Policy Compliance: Monitored via Intune
Device Status: Checked every 24 hours
Compliance State: Reported to Azure Monitor
Non-compliance: Alerted immediately
```

**Prevention:**
- Automatic policy enforcement
- Remote policy updates via Graph API
- Scheduled compliance verification
- Automated remediation actions

### TA0005: Defense Evasion

#### Continuous Policy Monitoring and Enforcement

**Implementation:**
- Continuous monitoring of policy compliance
- Detection of unauthorized configuration changes
- Automatic blocking of policy evasion attempts
- Real-time alerting for policy violations

**Detection:**
```yaml
Monitoring: Continuous policy compliance checks
Frequency: Daily automated scans
Alerts: Immediate notification on violations
Remediation: Automatic policy re-application
```

**Prevention:**
- Policy enforcement prevents unauthorized changes
- Audit logging of all configuration modifications
- Digital signatures for administrative commands
- Secure communication channels (TLS 1.3, AES-256)

## Detection Coverage Matrix

| Technique | Coverage | Tool | Status |
|-----------|----------|------|--------|
| TA0002 | Full | Microsoft Intune | Implemented |
| TA0005 | Full | Azure Monitor, Compliance Checks | Implemented |

## Defensive Recommendations

### Per Technique:

**TA0002 (Execution / Policy Enforcement):**
- Implement centralized policy management
- Use automated policy enforcement
- Enable real-time policy synchronization
- Deploy role-based access controls

**TA0005 (Defense Evasion Prevention):**
- Continuous compliance monitoring
- Automatic policy re-application
- Audit logging of all changes
- Secure administrative channels

## Implementation Overview

The system implements centralized policy management with automated compliance monitoring and remote control capabilities. Policies are assigned based on security groups through dynamic Azure AD groups, with automated compliance checks and user notifications.

## MITRE Navigator Layer

```json
{
  "name": "Case-005_Intune_Autopilot",
  "versions": {
    "attack": "13",
    "navigator": "4.9.1"
  },
  "techniques": [
    {
      "techniqueID": "TA0002",
      "color": "#66ff66",
      "comment": "Policy enforcement prevents unauthorized execution"
    },
    {
      "techniqueID": "TA0005",
      "color": "#66ff66",
      "comment": "Continuous monitoring prevents defense evasion"
    }
  ]
}
```

## Detection Signals

### Policy Compliance Indicators
- Device compliance state
- Policy synchronization status
- Configuration drift detection
- Unauthorized change attempts

### Behavioral Indicators
- Policy compliance failures
- Repeated non-compliance
- Unauthorized feature access
- Configuration changes outside normal hours

### System Indicators
- Intune compliance reports
- Azure Monitor alerts
- Policy assignment changes
- Device enrollment status

## Response Actions by Technique

### TA0002 (Execution / Policy Enforcement)
1. Centralized policy management via Intune
2. Automated policy enforcement
3. Real-time compliance monitoring
4. Automatic policy re-application

### TA0005 (Defense Evasion Prevention)
1. Continuous policy compliance checks
2. Detection of unauthorized changes
3. Automatic remediation actions
4. Secure audit logging

