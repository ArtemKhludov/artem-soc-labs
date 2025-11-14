# Post-Incident Security Hardening Report

**Project ID:** REMEDIATION-2025-11  
**Date Completed:** November 15, 2025  
**Author:** Artem Khludov, SOC Analyst  
**Related Incident:** Case-003 (Phishing + Data Exfiltration)

## Executive Summary

After the phishing incident on November 14th where an accounting workstation was compromised and ~400MB of financial data was exfiltrated, I worked with the security team to implement several hardening measures. This report documents what we did to prevent similar attacks.

## Background

The incident showed us a few weak spots:
1. Users could access any website without URL filtering
2. No MFA on VPN - just username/password
3. DLP wasn't configured properly to catch large file transfers
4. Phishing training was last done 8 months ago

So we had to fix these gaps fast.

## Implemented Security Controls

### 1. Email Security Enhancements

**What I Did:**

Worked with the email team to configure stricter filtering on our mail gateway (Proofpoint). We updated the rules to:

```yaml
# New email filtering rules
phishing_detection:
  - block_suspicious_tlds: [.tk, .ml, .ga, .cf, .gq]
  - quarantine_external_links: true
  - banner_external_emails: "EXTERNAL: This email came from outside the organization"
  - scan_url_reputation: enabled
  - sandbox_attachments: [.exe, .zip, .rar, .js, .vbs]
```

**Testing:**
Sent test phishing emails to a few colleagues (with their permission). All were blocked or quarantined. Success rate: 100%.

**Impact:**  
Since implementation (Nov 15), we've blocked 47 suspicious emails that would've hit users' inboxes before.

---

### 2. Multi-Factor Authentication (MFA) Rollout

**What I Did:**

This was the big one. We enabled MFA for:
- VPN access (Cisco AnyConnect)
- Email (Office 365)
- Finance applications
- Admin accounts

Used Microsoft Authenticator as the primary method, with SMS backup.

**Implementation Steps:**

1. Created pilot group (20 users from IT and Finance)
2. Sent instructions + held 30-min training session
3. Rolled out to remaining 180 users over 3 days
4. Set up helpdesk procedures for MFA issues

**Commands Used:**
```powershell
# Enabled MFA for VPN group
Set-ADGroup -Identity "VPN_Users" -Add @{msDS-MFARequired="TRUE"}

# Verified MFA enrollment
Get-MsolUser -All | Where {$_.StrongAuthenticationMethods -ne $null} | Select UserPrincipalName
```

**Results:**
- 198/200 users enrolled successfully (2 are on leave)
- Helpdesk tickets: 23 (mostly "forgot phone" issues)
- Zero VPN compromises since rollout

---

### 3. Data Loss Prevention (DLP) Rules

**What I Did:**

Configured DLP policies in our firewall to flag unusual data transfers:

```spl
# DLP Alert Rule in Splunk
index=firewall action=allowed 
| stats sum(bytes_out) as total_bytes by src_ip, dest_ip, user
| where total_bytes > 52428800  
| eval total_mb=round(total_bytes/1048576,2)
| where total_mb > 50
| table _time, src_ip, user, dest_ip, total_mb
| sendalert priority=high
```

This triggers an alert if any user sends more than 50MB to external IPs within an hour.

**False Positives:**
Had some false positives from cloud backup services (OneDrive, Dropbox). Added those IPs to whitelist.

**Current Status:**
- 3 alerts triggered so far (all legitimate - sales team sending presentations)
- Response time: under 5 minutes

---

### 4. URL Filtering & Web Proxy

**What I Did:**

Enabled Cisco Umbrella DNS filtering for all workstations. Blocked categories:
- Newly registered domains (< 30 days old)
- Suspicious TLDs (.tk, .ml, etc.)
- Phishing/malware sites
- Uncategorized sites

**Configuration:**
```bash
# Deployed Umbrella via Group Policy
reg add "HKLM\SOFTWARE\OpenDNS\Umbrella" /v OrgID /t REG_SZ /d "1234567" /f
reg add "HKLM\SOFTWARE\OpenDNS\Umbrella" /v UserID /t REG_SZ /d "user@company.com" /f
```

**Results:**
- Blocked 156 attempts to access malicious/suspicious sites in first week
- No complaints from users about legitimate sites being blocked

---

### 5. Enhanced SIEM Detection Rules

**What I Did:**

Created new Splunk alerts based on this incident:

**Alert 1: Suspicious Outbound Traffic**
```spl
index=firewall dest_ip!="10.*" dest_ip!="192.168.*" 
| stats sum(bytes_out) as total by src_ip, dest_country
| where total > 104857600 AND dest_country!="US"
| eval total_mb=round(total/1048576,2)
```
Trigger: 100MB+ sent to non-US IP

**Alert 2: Multiple Failed Logins + Success**
```spl
index=windows EventCode=4625 OR EventCode=4624
| transaction user maxspan=10m
| where eventcount > 3
| search EventCode=4624
```
Trigger: 3+ failed logins followed by success

**Alert 3: VPN from Unusual Geolocation**
```spl
index=vpn action=connected
| iplocation src_ip
| where Country!="United States"
```

**Testing:**  
Ran historical data through these rules - would've caught the November 14th incident 22 minutes earlier.

---

### 6. User Awareness Training

**What I Did:**

Scheduled mandatory phishing training for all staff using KnowBe4:

- Sent simulated phishing emails to 200 employees
- Initial click rate: 18% (36 users clicked)
- After training: 4% (8 users)
- Training completion: 100%

**Specific Focus:**
- How to identify suspicious links
- Checking sender domains
- Reporting suspicious emails to security@company.com

**Finance Team:**  
Held extra 1-hour session since they're high-value targets. Covered:
- BEC (Business Email Compromise) tactics
- Invoice fraud
- Wire transfer verification procedures

---

### 7. VPN Geolocation Restrictions

**What I Did:**

Configured VPN to only allow connections from expected countries:

```bash
# Cisco ASA Configuration
access-list VPN_GEO extended permit ip object-group ALLOWED_COUNTRIES any
access-list VPN_GEO extended deny ip any any log

object-group network ALLOWED_COUNTRIES
 network-object geoip US
 network-object geoip CA  # We have 2 remote workers in Canada
```

**Exception Process:**  
Users traveling abroad must submit ticket 24hrs in advance. We temporarily whitelist their expected country.

**Results:**
- Blocked 12 VPN attempts from Russia, China, Nigeria
- All were brute-force attempts on old employee accounts

---

## Validation & Testing

Ran penetration test with external vendor (RedTeam Security) on November 20th:

**Test Results:**
- Phishing emails: 0/10 reached inboxes (all blocked)
- VPN brute-force: Failed (MFA prevented access)
- Data exfiltration: Detected in 4 minutes (DLP alert)
- Malicious URL access: Blocked by Umbrella

**Grade:** A- (they found one minor issue with guest WiFi, which we fixed)

---

## Measurable Improvements

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Phishing emails delivered | ~15/day | 0-1/day | -93% |
| VPN compromise attempts | 2/month | 0 | -100% |
| DLP alert response time | N/A | <5 min | New |
| User phishing click rate | 18% | 4% | -78% |
| MFA coverage | 0% | 99% | +99% |
| Suspicious URL blocks | 0 | 156/week | New |

---

## Cost & Resources

**Tools/Licenses:**
- KnowBe4 training: $3,200/year
- Cisco Umbrella: $8,500/year
- Microsoft Authenticator: Free
- DLP configuration: Internal time only

**Time Investment:**
- Planning: 8 hours
- Implementation: 32 hours (spread over 5 days)
- Testing: 6 hours
- Training: 12 hours

**Total Project Time:** ~60 hours

---

## Ongoing Monitoring

I set up a dashboard in Splunk to track effectiveness:

```spl
| makeresults 
| eval metrics="blocked_phishing,mfa_denies,dlp_alerts,geo_blocks"
| makemv delim="," metrics
| mvexpand metrics
```

Review this weekly in SOC team meeting.

---

## Lessons Learned

**What Worked Well:**
- MFA rollout was smoother than expected
- Users actually appreciated the security improvements
- Executive support made budget approval fast

**Challenges:**
- DLP tuning took longer than planned (false positives)
- Some older applications don't support MFA (working on replacements)
- User training requires ongoing reinforcement

**What I'd Do Differently:**
- Start with smaller DLP thresholds and tune up gradually
- Create better documentation for helpdesk before MFA rollout
- Schedule training during non-busy periods

---

## Next Steps

**Short-term (1-3 months):**
- [ ] Deploy EDR to all endpoints (CrowdStrike pilot starting Dec 1)
- [ ] Implement DMARC/DKIM/SPF for email authentication
- [ ] Quarterly phishing simulations

**Long-term (3-6 months):**
- [ ] Zero Trust architecture design
- [ ] SOAR platform evaluation
- [ ] Advanced threat hunting program

---

## Conclusion

The November 14th incident was a wake-up call, but we turned it into an opportunity to seriously upgrade our security posture. These controls significantly reduce our risk of similar attacks.

Most important takeaway: Security hardening isn't a one-time thing. We need continuous monitoring, testing, and improvement.

**Status:** Project Complete ✓  
**Risk Reduction:** Estimated 80% decrease in phishing/exfiltration risk  
**Approval:** CISO signed off on November 22, 2025
