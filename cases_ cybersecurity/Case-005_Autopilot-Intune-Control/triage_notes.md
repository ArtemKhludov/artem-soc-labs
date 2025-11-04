# Case 005: Centralized Policy Management via Intune / Autopilot

**Date:** November 2025  
**Analyst:** Artem Khludov  
**Company:** EnergyLogic AI  
**Severity:** MEDIUM  
**Status:** Implemented

## Executive Summary

I built a centralized system for managing device settings, security policies, and access permissions through Microsoft Intune and Autopilot. The goal was to simplify daily operations, strengthen security, and enable full remote management of features, user access, and policy changes. All policies can be automatically checked and verified in real time without manual intervention.

## Timeline

| Date | Event | Status |
|------|-------|--------|
| Nov 1, 2025 | Identified core policies and created base Intune profiles for different security groups | Planning |
| Nov 2, 2025 | Integrated all devices into Intune and Autopilot using dynamic groups | Implementation |
| Nov 3, 2025 | Built PowerShell scripts to automatically verify compliance and send notifications to users when policies were out of sync | Automation |
| Nov 4, 2025 | Set up centralized control panel for policy and access management | Deployment |
| Nov 5, 2025 | Completed testing of remote activation and deactivation of features and policies | Completed |

## Project Overview

### 1. Centralized Policy Management
- **Method:** Microsoft Intune configuration profiles
- **Target:** All corporate devices across multiple departments
- **Approach:** Role-based policy assignment through dynamic groups
- **Scope:** Multiple departments with different security requirements

### 2. Automated Compliance Monitoring
- **Tools:** PowerShell scripts with Azure Automation
- **Frequency:** Scheduled checks via Azure Automation Runbooks
- **Alerting:** Email notifications to users and IT admins
- **Logging:** Azure Monitor integration with SOC dashboard

### 3. Remote Feature Control
- **API:** Microsoft Graph API for remote policy management
- **Capabilities:** Real-time enable/disable of features, VPN, SaaS apps, access rules
- **Security:** All commands digitally signed and stored in secure audit logs
- **Encryption:** TLS 1.3 and AES-256 for all communications

## Implementation Details

### Policy Configuration Examples

Different departments received tailored security profiles based on their access requirements:
- High-security departments: Restricted VPN, MFA required, no external access
- Standard departments: Standard VPN access, medium security baseline
- Development teams: Full VPN access with development tools enabled
- Administrative roles: Full access with enhanced monitoring and encrypted communications

### Intune Profile Structure
- Configuration profiles per security group
- Compliance policies with automatic enforcement
- Security baseline configurations
- Endpoint protection settings

### Autopilot Integration
- Automatic device enrollment on first login
- Pre-configured settings based on security groups
- Zero-touch deployment for new devices
- Automatic policy assignment through dynamic groups

## Tools and Techniques

### Microsoft Intune
- Policy profiles for device configuration
- Compliance checks with automatic remediation
- Group-based configuration using RBAC
- Real-time policy synchronization

### Windows Autopilot
- Automatic device enrollment
- First-login setup automation
- Role-based profile assignment
- Remote device provisioning

### PowerShell Automation
- Scheduled compliance verification scripts
- User notification system
- Policy status reporting
- Automated remediation actions

### Azure AD Dynamic Groups
- Automatic policy assignment based on user role
- Role-based group membership
- Dynamic device grouping
- RBAC integration

### Microsoft Graph API
- Remote feature toggle functionality
- Policy assignment and updates
- Device management operations
- Audit log retrieval

### Security Measures
- TLS 1.3 encryption for all communications
- AES-256 encryption for sensitive data
- Digital signatures for administrative commands
- Secure audit log storage in Azure Key Vault

## Detection and Monitoring

### Data Sources
- Intune compliance reports
- Azure Log Analytics
- Azure Monitor alerts
- SOC dashboard integration

### Trigger Conditions
- Non-compliant device detected
- Unauthorized feature change
- Device not synced for over 48 hours
- Policy compliance failure

### Alerting Mechanisms
- Email notification to user and IT admin
- Teams notification for critical issues
- Automatic IT ticket creation after repeated non-compliance
- SOC dashboard alerts for policy violations

## Implementation Steps

### Day 1 (Nov 1, 2025): Policy Identification and Profile Creation

I started by analyzing the existing device configurations and identifying what policies needed to be centralized. I reviewed different security requirements across departments and mapped them to Intune configuration profiles.

**Process:**
1. I analyzed current device configurations and access requirements
2. I identified core policies needed for different security groups
3. I created base Intune profiles in the Intune admin center
4. I configured security baseline settings for each profile
5. I set up endpoint protection policies for all groups

**Result:** Base Intune profiles created for multiple security groups with appropriate security baselines.

### Day 2 (Nov 2, 2025): Device Integration and Dynamic Groups

I integrated all existing devices into Intune and Autopilot, and configured dynamic groups for automatic policy assignment.

**Process:**
1. I enrolled existing devices into Intune using Company Portal
2. I configured Windows Autopilot profiles for automatic enrollment of new devices
3. I created Azure AD dynamic groups based on user roles and departments
4. I assigned Intune profiles to the appropriate dynamic groups
5. I verified that devices were receiving policies correctly

**Result:** All devices integrated into Intune, dynamic groups configured for automatic policy assignment.

### Day 3 (Nov 3, 2025): Automation Scripts Development

I built PowerShell scripts to automatically verify compliance and send notifications to users when their policies were out of sync.

**Process:**
1. I wrote PowerShell scripts using Microsoft Graph API to check device compliance status
2. I integrated the scripts with Azure Automation for scheduled execution
3. I configured email notifications to users when devices fall out of compliance
4. I set up Azure Monitor alerts for IT admins
5. I tested the scripts on a subset of devices first

**Result:** Automated compliance checking system operational with user notifications and IT alerts.

### Day 4 (Nov 4, 2025): Centralized Control Panel Setup

I set up a centralized control panel for policy and access management that allows real-time control over features and policies.

**Process:**
1. I created a web-based dashboard using Microsoft Graph API
2. I integrated policy management functions into the dashboard
3. I configured remote feature toggle capabilities (VPN, SaaS apps, access rules)
4. I set up secure authentication for administrative access
5. I configured audit logging for all administrative actions

**Result:** Centralized control panel operational with remote policy management capabilities.

### Day 5 (Nov 5, 2025): Testing and Validation

I completed testing of remote activation and deactivation of features and policies to ensure everything works correctly.

**Process:**
1. I tested remote policy assignment via Graph API
2. I verified compliance alerts work correctly for non-compliant devices
3. I tested remote feature enable/disable functionality
4. I validated that all administrative actions are properly logged
5. I confirmed that user notifications are sent correctly
6. I tested policy enforcement on sample devices

**Result:** All functionality tested and validated, system ready for production use.

## Lessons Learned

**Successful actions:**
- Automated scripts made it much easier to detect non-compliance early and fix issues quickly
- Centralized management through Intune eliminated manual setup mistakes and gave me full visibility
- Adding Graph API control and cryptographic validation ensured no one could fake or alter administrative commands
- Dynamic groups simplified policy assignment and reduced administrative overhead

**Areas for improvement:**
- Need better integration with Microsoft Sentinel for automated incident response
- Should implement more granular compliance reporting
- Plan to add proactive monitoring for policy drift
- Want to expand automated remediation capabilities

## Recommendations

1. **Immediate:**
   - Integrate with Microsoft Sentinel for automated compliance analytics
   - Expand automated remediation actions
   - Add more granular compliance reporting

2. **Short-term:**
   - Implement proactive monitoring for policy drift
   - Add machine learning for anomaly detection
   - Create automated compliance dashboards

3. **Long-term:**
   - Expand to mobile device management
   - Implement zero-trust architecture principles
   - Add automated security posture assessment

## MITRE ATT&CK Mapping

- **TA0002:** Execution / Policy Enforcement - Prevents unauthorized system changes
- **TA0005:** Defense Evasion - Continuous policy monitoring helps detect and stop evasion attempts

## Supporting Evidence

- Intune configuration profiles
- PowerShell automation scripts
- Graph API integration code
- Compliance reports and logs
- Azure Monitor alerts and dashboards

## Scripts and Configuration

### Policy Compliance Check Script
```powershell
$devices = Get-IntuneManagedDevice
foreach ($device in $devices) {
    $policy = Get-IntuneDeviceConfigurationPolicyStatus -DeviceId $device.Id
    if ($policy.Status -ne "Compliant") {
        Send-MailMessage -To $device.UserEmail -Subject "Device Policy Alert" `
        -Body "Your device is out of compliance. Please contact IT or sync policies." `
        -SmtpServer "smtp.office365.com" -UseSsl
    }
}
```

### Remote Feature Control via Graph API
```
POST https://graph.microsoft.com/v1.0/deviceManagement/configurations/{policyId}/assign
Headers:
  Authorization: Bearer {token}
Body:
  {
    "target": {
      "groupId": "SecurityGroup-Restricted"
    }
  }
```

## User Guidance

**For non-technical staff:**
1. If you get a "Policy out of compliance" message, open Company Portal and sync your device
2. If it happens again, create a quick IT ticket and I'll fix it remotely
3. New apps or permissions can be requested via the internal IT form
4. All policies update automatically, no manual setup required

## Success Metrics

- **Centralized Control:** Full centralized control of all device and access policies
- **Remote Management:** Real-time remote feature management enabled
- **Automation:** Automatic user alerts for compliance issues
- **Security:** Secure, encrypted audit of all administrative changes
- **Visibility:** Stronger visibility and higher overall security posture

## Follow-up Actions

- [ ] I will integrate with Microsoft Sentinel for automated compliance analytics
- [ ] I will implement proactive monitoring for policy drift detection
- [ ] I will expand automated remediation capabilities
- [ ] I will create monthly compliance reports for management

**Reported to:** IT Director, Security Manager, CISO  
**Follow-up required:** Microsoft Sentinel integration for automated monitoring  
**Status:** Implemented - System fully operational

_Last updated: 2025-11-05_
