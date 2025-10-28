# MITRE ATT&CK Mapping - Case 004: Cloudflare Spam Form Submissions

## Attack Chain Overview

```
Initial Access  Execution  Impact
    T1190         T1059      T1499
```

## Detailed Technique Mapping

### TA0001: Initial Access

#### T1190 - Exploit Public-Facing Application
**Sub-technique:** T1190.001 - Web Applications

**Evidence:**
- Direct API access to Calendly endpoints bypassing website
- Automated form submissions to /booking and /calendly endpoints
- Missing Referer and Origin headers indicating direct API calls

**Detection:**
```
HTTP Method: POST
URI Path: /calendly, /booking
Headers: Referer: "", Origin: not from example.com
Bot Score: <30
```

**Prevention:**
- Implement proper API authentication
- Validate Referer/Origin headers
- Use Cloudflare Turnstile for form protection

### TA0002: Execution

#### T1059 - Command and Scripting Interpreter
**Sub-technique:** T1059.009 - Cloud APIs

**Evidence:**
- Automated scripts targeting Calendly API endpoints
- Sequential timestamps indicating scripted behavior
- Identical User-Agent strings across multiple requests

**Detection:**
```yaml
Pattern: Sequential POST requests
Interval: Uniform timing (every 2-3 seconds)
User-Agent: "python-requests/2.28.1", "curl/7.68.0"
ASN: 14061, 9009, 208091 (VPS providers)
```

**Prevention:**
- Rate limiting on API endpoints
- Bot detection and management
- API key authentication requirements

### TA0040: Impact

#### T1499 - Endpoint Denial of Service
**Sub-technique:** T1499.004 - Application or System Exploitation

**Evidence:**
- Hundreds of fake demo booking requests per hour
- Resource consumption on Calendly infrastructure
- Potential impact on legitimate user experience

**Detection:**
```yaml
Volume: 100+ requests per hour
Pattern: Automated form submissions
Impact: Resource hijacking, service degradation
```

**Prevention:**
- Cloudflare Bot Management
- Rate limiting and throttling
- CAPTCHA/Turnstile challenges

## Detection Coverage Matrix

| Technique | Coverage | Tool | Status |
|-----------|----------|------|--------|
| T1190 | Full | Cloudflare WAF | Detected |
| T1059.009 | Full | Bot Management | Detected |
| T1499.004 | Full | Rate Limiting | **BLOCKED** |

## Defensive Recommendations

### Per Technique:

**T1190 (Exploit Public-Facing Application):**
- Implement proper API authentication
- Validate all HTTP headers (Referer, Origin)
- Use Cloudflare WAF rules to block direct API access
- Deploy Turnstile on all form endpoints

**T1059 (Command and Scripting Interpreter):**
- Enable Cloudflare Bot Management
- Implement JA3/TLS fingerprinting
- Monitor for automated tool signatures
- Use behavioral analysis for detection

**T1499 (Endpoint Denial of Service):**
- Deploy rate limiting (3 requests per 10 seconds)
- Use managed challenges for suspicious traffic
- Monitor resource consumption
- Implement circuit breakers

## Threat Actor Profile

**TTP Similarity:**
- Automated spam bots
- VPS-based attack infrastructure
- Common scraping tools (python-requests, curl)

**Attribution Confidence:** Low (common automated tools)

## Cloudflare-Specific Detection Rules

### WAF Rule 1: Block Missing Headers
```yaml
rule_name: "Block Spam Forms - Missing Headers"
expression: |
  (http.request.method eq "POST" and http.request.uri.path contains "/calendly")
  and (http.request.headers["referer"][0] eq "" or not http.request.headers["origin"][0] contains "example.com")
action: block
```

### WAF Rule 2: Bot Score Filtering
```yaml
rule_name: "Block Low Bot Score Requests"
expression: |
  http.request.method eq "POST" and 
  http.request.uri.path contains "/booking" and
  cf.bot_management.score < 30
action: managed_challenge
```

### WAF Rule 3: ASN Blocking
```yaml
rule_name: "Block VPS ASNs"
expression: |
  http.request.method eq "POST" and 
  (http.request.uri.path contains "/calendly" or http.request.uri.path contains "/booking") and
  ip.geoip.asnum in {14061, 9009, 208091}
action: block
```

## MITRE Navigator Layer

```json
{
  "name": "Case-004_Cloudflare_SpamForms",
  "versions": {
    "attack": "13",
    "navigator": "4.9.1"
  },
  "techniques": [
    {
      "techniqueID": "T1190",
      "color": "#ff6666",
      "comment": "Direct API access to Calendly endpoints"
    },
    {
      "techniqueID": "T1059.009",
      "color": "#ff6666",
      "comment": "Automated scripts targeting form endpoints"
    },
    {
      "techniqueID": "T1499.004",
      "color": "#66ff66",
      "comment": "Spam blocked by Cloudflare WAF and Bot Management"
    }
  ]
}
```

## IOCs and Detection Signals

### Network Indicators
- **ASNs:** 14061, 9009, 208091 (VPS providers)
- **User-Agents:** "python-requests/2.28.1", "curl/7.68.0"
- **Headers:** Missing Referer, empty Origin

### Behavioral Indicators
- Sequential timestamps (uniform intervals)
- Identical JA3/TLS fingerprints
- No cookie persistence
- High request frequency

### Cloudflare-Specific Indicators
- Bot Score < 30
- Missing Turnstile tokens
- Direct API access patterns
- VPS-based infrastructure

## Response Actions by Technique

### T1190 (Exploit Public-Facing Application)
1. Implement WAF rules blocking missing headers
2. Deploy Turnstile on all form endpoints
3. Validate Origin/Referer headers
4. Monitor for direct API access patterns

### T1059 (Command and Scripting Interpreter)
1. Enable Cloudflare Bot Management
2. Implement JA3 fingerprinting
3. Deploy managed challenges
4. Monitor for automated tool signatures

### T1499 (Endpoint Denial of Service)
1. Implement rate limiting
2. Deploy circuit breakers
3. Monitor resource consumption
4. Use adaptive challenges

## References

- [MITRE ATT&CK - T1190](https://attack.mitre.org/techniques/T1190/)
- [MITRE ATT&CK - T1059](https://attack.mitre.org/techniques/T1059/)
- [MITRE ATT&CK - T1499](https://attack.mitre.org/techniques/T1499/)
- [Cloudflare Bot Management](https://developers.cloudflare.com/bots/)
- [Cloudflare WAF Rules](https://developers.cloudflare.com/waf/)

_Date: 2025-10-28_
