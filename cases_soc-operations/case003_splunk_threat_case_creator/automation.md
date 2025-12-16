# Automation & Tuning (Case-003)

This section is what I would normally deliver to a client as “how to keep it quiet and useful”.

## 1) Correlation searches (scheduled)
I structured detections as scheduled searches that produce a consistent output:
- key fields: `src_ip`, `user`, `host`, `uri_path`, `severity`
- a short `rule_name` field so it’s easy to route downstream

### Why it matters
When every alert has the same shape, it becomes easy to:
- deduplicate incidents
- build dashboards
- send clean ticket payloads

## 2) Throttling / suppression (noise control)
For noisy sources (login failures) I used throttling logic:
- throttle by `src_ip` (and sometimes `user`) for 30–60 minutes
- only alert if the count crosses the threshold again

In a real Splunk ES environment this maps to “notable event suppression” / “throttle” settings.

## 3) Lookup-based allowlists and watchlists
I used lookups as the simplest maintainable tuning tool.

### Allowlist
- office egress IPs
- known vulnerability scanners
- synthetic monitoring

### Watchlist
- suspicious IPs seen in multiple detections
- suspicious user agents

**Pattern** (conceptually):
- enrich events with `lookup allowlist.csv src_ip OUTPUT is_allowed`
- `where isnull(is_allowed)` before alerting

## 4) Alert actions (ticket payload template)
Even if the “action” is just email/webhook, the content needs to be structured.

Example fields I include:
- `rule_name`
- `severity`
- `src_ip`
- `user` (if present)
- `host` (if present)
- counts (`failed_logins`, `waf_auth_fails`)
- timeframe (`first_seen`, `last_seen`)
- recommended next steps (short)

This makes it easy to push to:
- Slack / Teams
- Jira / ServiceNow
- a SOAR platform later

## 5) Simple risk scoring (RBA-lite)
If the client doesn’t have full Risk-Based Alerting, I still do a light version:
- WAF login abuse: +20
- Windows spray: +30
- Success-after-fail: +40
- admin group change: +80

Then alert when `risk_score >= 60`.

## 6) Automation outside Splunk (Python helper)
I added `log_generator.py` to:
- generate realistic Windows + WAF events (JSONL)
- quickly validate that the detections actually trigger
- produce quick stats (top IPs, counts by code/status)

This is useful in real work because it reduces back-and-forth during tuning.

## 7) Where I used AI (and how I validated)
I explicitly used AI (ChatGPT) for:
- drafting SPL alternatives (stats vs tstats patterns)
- generating realistic test scenarios and edge cases
- polishing documentation into a client-friendly format

But I never shipped AI output “blind”. I validated by:
- running each search on known test data
- checking false positive sources (allowlists)
- testing thresholds (low/high) and picking sane defaults
