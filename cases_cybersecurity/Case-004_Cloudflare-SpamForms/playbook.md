# Incident Response Playbook: Cloudflare Spam Form Submissions

**Playbook ID:** IR-PB-004  
**Version:** 1.0  
**Last Updated:** 2025-10-28  
**Author:** Artem Khludov, SOC Analyst

## Playbook Overview

| Field | Value |
|-------|-------|
| **Incident Type** | Automated Spam Form Submissions |
| **MITRE Tactic** | Impact (TA0040) |
| **Severity** | HIGH |
| **Estimated Time** | 30-60 minutes |
| **Required Tools** | Cloudflare Dashboard, Logpull API, WAF Rules, Bot Management |

## Trigger Conditions

This playbook is activated when:

- [ ] 50+ form submissions per hour from automated sources
- [ ] Missing or empty Referer/Origin headers in form requests
- [ ] Identical User-Agent strings across multiple submissions
- [ ] Sequential timestamps from same ASN/IP ranges
- [ ] Low BotScore (<30) for form submissions
- [ ] Direct API access to form endpoints bypassing website

## Response Workflow

### Phase 1: Detection & Analysis (0-10 minutes)

#### Step 1: Validate the Alert

```bash
# Check Cloudflare Analytics for form endpoint traffic
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/analytics/dashboard" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  --data '{"since":"2025-10-28T00:00:00Z","until":"2025-10-28T23:59:59Z"}'
```

**Decision Point:**
- **True Positive:** High volume + missing headers + low bot score  Proceed to Phase 2
- **False Positive:** Legitimate traffic patterns  Close alert

#### Step 2: Analyze Traffic Patterns

**Information to Gather:**
- [ ] Form endpoint being targeted (/booking, /calendly)
- [ ] Source IPs and ASNs
- [ ] User-Agent patterns
- [ ] Referer/Origin header analysis
- [ ] BotScore distribution
- [ ] Request frequency and timing

**Cloudflare Logpull Query:**
```bash
# Export logs for analysis
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/logpull/requests" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  --data '{
    "start_time": "2025-10-28T00:00:00Z",
    "end_time": "2025-10-28T23:59:59Z",
    "fields": ["RayID","EdgeStartTimestamp","ClientIP","ClientRequestURI","ClientRequestMethod","ClientRequestUserAgent","ClientRequestReferer","ClientRequestOrigin","BotScore","ASN","Country"]
  }'
```

### Phase 2: Immediate Mitigation (10-20 minutes)

#### Step 3: Implement WAF Rules

**Rule 1: Block Missing Headers**
```yaml
# Cloudflare WAF Rule
rule_name: "Block Spam Forms - Missing Headers"
expression: |
  (http.request.method eq "POST" and http.request.uri.path contains "/calendly")
  and (http.request.headers["referer"][0] eq "" or not http.request.headers["origin"][0] contains "example.com")
action: block
```

**Rule 2: Rate Limiting**
```yaml
# Rate Limiting Rule
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

#### Step 4: Enable Bot Management

**Super Bot Fight Mode:**
```bash
# Enable Bot Management
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{zone_id}/bot_management" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  --data '{
    "enable_js": true,
    "enable_cookie": true,
    "enable_challenge": true
  }'
```

#### Step 5: Deploy Cloudflare Turnstile

**Turnstile Configuration:**
```html
<!-- Add to form pages -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<div class="cf-turnstile" data-sitekey="YOUR_SITE_KEY"></div>
```

### Phase 3: Advanced Detection (20-30 minutes)

#### Step 6: Implement JA3/TLS Fingerprint Analysis

**Custom Rule for TLS Fingerprinting:**
```yaml
rule_name: "Block Identical TLS Fingerprints"
expression: |
  http.request.method eq "POST" and 
  http.request.uri.path contains "/calendly" and
  cf.bot_management.score < 30 and
  http.tls.ja3_fingerprint in ["known_bot_fingerprint_1", "known_bot_fingerprint_2"]
action: block
```

#### Step 7: Cookie and Session Validation

**Session Consistency Check:**
```yaml
rule_name: "Block Session Replay Attacks"
expression: |
  http.request.method eq "POST" and 
  http.request.uri.path contains "/booking" and
  http.request.headers["cookie"][0] eq "" and
  cf.bot_management.score < 30
action: challenge
```

### Phase 4: Monitoring & Tuning (30-45 minutes)

#### Step 8: Set Up Monitoring

**Cloudflare Analytics Dashboard:**
```bash
# Create custom dashboard query
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/analytics/dashboard" \
  -H "Authorization: Bearer {api_token}" \
  --data '{
    "query": {
      "dimensions": ["ClientIP", "ClientRequestURI", "BotScore"],
      "filters": "ClientRequestMethod eq POST and ClientRequestURI contains /calendly",
      "since": "2025-10-28T00:00:00Z",
      "until": "2025-10-28T23:59:59Z"
    }
  }'
```

#### Step 9: Fine-tune Rules

**Adjust Bot Score Threshold:**
```yaml
# Refined rule based on monitoring
rule_name: "Adaptive Bot Detection"
expression: |
  http.request.method eq "POST" and 
  http.request.uri.path contains "/calendly" and
  cf.bot_management.score < 25 and
  (http.request.headers["referer"][0] eq "" or 
   not http.request.headers["origin"][0] contains "example.com" or
   http.request.headers["cookie"][0] eq "")
action: managed_challenge
```

### Phase 5: Validation & Cleanup (45-60 minutes)

#### Step 10: Verify Effectiveness

**Success Metrics:**
- [ ] Spam submissions reduced by >90%
- [ ] Legitimate users not affected
- [ ] No false positives in Security Events
- [ ] Bot Management scoring working correctly

**Validation Commands:**
```bash
# Check Security Events
curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/security/events" \
  -H "Authorization: Bearer {api_token}" \
  --data '{
    "since": "2025-10-28T10:00:00Z",
    "until": "2025-10-28T12:00:00Z",
    "action": "managed_challenge,block"
  }'
```

#### Step 11: Document IOCs

**IOC Collection:**
```yaml
# Known malicious ASNs
asns:
  - 14061  # VPS provider
  - 9009   # VPS provider  
  - 208091 # VPS provider

# Known bot User-Agents
user_agents:
  - "python-requests/2.28.1"
  - "curl/7.68.0"
  - "Mozilla/5.0 (compatible; Bot/1.0)"

# TLS Fingerprints
tls_fingerprints:
  - "known_bot_ja3_hash_1"
  - "known_bot_ja3_hash_2"
```

## Decision Tree

```
Spam Form Alert
    ├── High Volume (>50/hour)?
    │   ├── Yes  Check Headers
    │   │   ├── Missing Referer/Origin?  HIGH Priority
    │   │   └── Present  Check Bot Score
    │   │       ├── <30  HIGH Priority
    │   │       └── >30  MEDIUM Priority
    │   └── No  Monitor
    │
    ├── Direct API Access?
    │   ├── Yes  CRITICAL - Implement WAF rules
    │   └── No  Check legitimate form flow
    │
    └── Identical Patterns?
        ├── Yes  Block ASN/IP ranges
        └── No  Individual IP analysis
```

## Escalation Path

| Severity | Notify | Timeline |
|----------|--------|----------|
| **CRITICAL** | SOC Manager, CISO, Marketing Team | Immediate |
| **HIGH** | SOC Lead, Security Engineer | 15 minutes |
| **MEDIUM** | SOC Analyst (L2) | 30 minutes |

## Tools Reference

| Tool | Purpose | Command |
|------|---------|---------|
| Cloudflare API | Log analysis | `curl -X GET "https://api.cloudflare.com/client/v4/zones/{zone_id}/logpull/requests"` |
| WAF Rules | Traffic filtering | Custom expressions in Cloudflare Dashboard |
| Bot Management | Automated detection | Enable Super Bot Fight Mode |
| Turnstile | CAPTCHA alternative | Deploy on form pages |

## Response Checklist

- Alert validated
- Traffic patterns analyzed
- WAF rules implemented
- Bot Management enabled
- Turnstile deployed
- Rate limiting configured
- Monitoring set up
- Rules fine-tuned
- Effectiveness verified
- IOCs documented
- False positives checked
- Report created

## References

- [Cloudflare WAF Rules](https://developers.cloudflare.com/waf/)
- [Cloudflare Bot Management](https://developers.cloudflare.com/bots/)
- [Cloudflare Turnstile](https://developers.cloudflare.com/turnstile/)
- [MITRE ATT&CK - T1499](https://attack.mitre.org/techniques/T1499/)

Applied to Case-004 on 2025-10-28 (response: 30 min).
