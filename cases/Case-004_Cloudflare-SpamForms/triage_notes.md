# Case 004: Cloudflare Spam Form Submissions

**Date:** October 28, 2025  
**Analyst:** Artem Khludov  
**Company:** EnergyLogic AI  
**Severity:** HIGH  
**Status:** Resolved

## Executive Summary

Responded to automated spam form submissions targeting Calendly booking endpoints. Identified direct API access bypassing website forms, implemented Cloudflare WAF rules and Bot Management, reducing spam by 98% while maintaining legitimate user experience.

## Timeline

| Time | Event | Status |
|------|-------|--------|
| 09:45 | Report received about abnormal spike in demo bookings | Alert |
| 10:00 | Pulled Cloudflare logs using Logpull API (48-hour range) | Analysis |
| 10:20 | Found repetitive patterns: empty headers, identical UAs, sequential timestamps | Identified |
| 10:30 | Confirmed traffic hitting Calendly directly, not through embedded form | Confirmed |
| 10:45 | Implemented rate-limiting rules and JavaScript challenge | Mitigation |
| 11:15 | Activated Bot Management and Cloudflare Turnstile | Enhanced |
| 11:30 | Spam activity dropped by 98% | Resolved |

## Attack Analysis

### 1. Attack Vector (T1190)
- **Method:** Direct API access to Calendly endpoints
- **Target:** /booking and /calendly form endpoints
- **Bypass:** Missing Referer and Origin headers
- **Volume:** 100+ submissions per hour

### 2. Automation Indicators (T1059)
- **Tools:** python-requests, curl, automated scripts
- **Pattern:** Sequential timestamps (every 2-3 seconds)
- **Infrastructure:** VPS providers (ASN: 14061, 9009, 208091)
- **Behavior:** No cookie persistence, identical User-Agents

### 3. Impact Assessment (T1499)
- **Resource Consumption:** High volume hitting Calendly infrastructure
- **User Experience:** Potential degradation of legitimate bookings
- **Business Impact:** Spam filling up demo booking slots

## IOC (Indicators of Compromise)

### Network Indicators
- **Malicious ASNs:** 14061, 9009, 208091 (VPS providers)
- **User-Agents:** "python-requests/2.28.1", "curl/7.68.0"
- **Headers:** Missing Referer, empty Origin headers
- **Patterns:** Sequential timestamps, uniform intervals

### Behavioral Indicators
- **Bot Score:** <30 (Cloudflare Bot Management)
- **TLS Fingerprints:** Identical JA3 hashes across different IPs
- **Session Data:** No cookies, no session persistence
- **Request Frequency:** 3+ requests per 10 seconds per IP

### Cloudflare-Specific Indicators
- **Direct API Access:** Bypassing website form validation
- **Missing Turnstile Tokens:** No CAPTCHA validation
- **Low Bot Score:** Automated traffic detection
- **VPS Infrastructure:** Known hosting providers

## Detection Logic

### Cloudflare WAF Rule 1
```yaml
rule_name: "Block Spam Forms - Missing Headers"
expression: |
  (http.request.method eq "POST" and http.request.uri.path contains "/calendly")
  and (http.request.headers["referer"][0] eq "" or not http.request.headers["origin"][0] contains "example.com")
action: block
```

### Cloudflare WAF Rule 2
```yaml
rule_name: "Block Low Bot Score Requests"
expression: |
  http.request.method eq "POST" and 
  http.request.uri.path contains "/booking" and
  cf.bot_management.score < 30
action: managed_challenge
```

### Rate Limiting Rule
```yaml
rule_name: "Form Submission Rate Limit"
expression: |
  http.request.method eq "POST" and 
  (http.request.uri.path contains "/booking" or http.request.uri.path contains "/calendly")
action: rate_limit
rate_limit:
  requests_per_period: 3
  period_seconds: 10
  action: challenge
```

## Response Actions

### Immediate (0-15 min)
- [x] Analyzed Cloudflare logs using Logpull API
- [x] Identified attack patterns and source infrastructure
- [x] Confirmed direct API access bypassing website forms

### Short-term (15-30 min)
- [x] Implemented WAF rules blocking missing headers
- [x] Deployed rate limiting (3 requests per 10 seconds)
- [x] Enabled Cloudflare Bot Management (Super Bot Fight Mode)
- [x] Activated Cloudflare Turnstile on form endpoints

### Long-term (30-60 min)
- [x] Fine-tuned rules based on false positive analysis
- [x] Implemented JA3/TLS fingerprint analysis
- [x] Set up continuous monitoring and alerting
- [x] Documented IOCs and response procedures

## Root Cause Analysis

1. **Missing API Authentication:** Calendly endpoints accessible without proper validation
2. **No Bot Detection:** Lack of automated traffic filtering
3. **Missing Headers Validation:** No Referer/Origin header checks
4. **No Rate Limiting:** Unlimited form submissions allowed
5. **Direct API Access:** Attackers bypassing website form controls

## Lessons Learned

**What worked:**
- Cloudflare Logpull API provided excellent visibility into attack patterns
- WAF rules effectively blocked automated traffic
- Bot Management accurately identified bot behavior
- Turnstile provided better user experience than traditional CAPTCHA

**What needs improvement:**
- Initial rules were too restrictive for corporate VPNs
- Need better false positive monitoring
- Should implement behavioral analysis earlier
- Need automated IOC sharing with threat intelligence

## Recommendations

1. **Immediate:**
   - Deploy Turnstile on all form endpoints
   - Implement proper API authentication
   - Enable Bot Management on all public-facing forms

2. **Short-term:**
   - Add behavioral analysis to WAF rules
   - Implement JA3 fingerprinting for bot detection
   - Set up automated monitoring and alerting

3. **Long-term:**
   - Deploy AI-based anomaly detection
   - Implement threat intelligence integration
   - Regular purple team exercises for form security

## MITRE ATT&CK Mapping

- **T1190:** Exploit Public-Facing Application (Initial Access)
- **T1059.009:** Command and Scripting Interpreter - Cloud APIs (Execution)
- **T1499.004:** Endpoint Denial of Service - Application Exploitation (Impact)

## Supporting Evidence

- Cloudflare log exports (48-hour analysis)
- WAF rule configurations
- Bot Management analytics
- Rate limiting statistics
- Turnstile validation logs

## False Positive Analysis

**Initial Issues:**
- Corporate VPN traffic blocked due to strict IP rate limits
- Some legitimate users challenged by Bot Management

**Resolution:**
- Added cookie and fingerprint checks to rules
- Refined Bot Score thresholds
- Implemented whitelist for known good traffic

## Success Metrics

- **Spam Reduction:** 98% decrease in automated submissions
- **False Positives:** <1% of legitimate users affected
- **Response Time:** 30 minutes from detection to resolution
- **User Experience:** No impact on legitimate form submissions

## Follow-up Actions

- [ ] Weekly review of Cloudflare analytics
- [ ] Monthly rule tuning based on traffic patterns
- [ ] Quarterly security assessment of form endpoints
- [ ] Annual penetration testing of form security

**Reported to:** Security Manager, Marketing Team, CISO  
**Follow-up required:** 30-day review of Bot Management effectiveness  
**Status:** Closed - Spam successfully mitigated

_Last updated: 2025-10-28_
