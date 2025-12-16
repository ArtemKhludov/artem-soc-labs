# SOC Case-003: Splunk SIEM Threat Case Creator (Upwork Simulation)

**Date:** December 14, 2025  
**Analyst:** Artem Khludov  
**Context:** Simulated Upwork engagement (“Splunk SIEM Threat Case Creator Needed”)  
**Platform:** Splunk (Enterprise / Cloud-style approach)  
**Data sources:** Windows Security logs + Web/WAF logs

## Objective
Deliver a small but realistic set of Splunk threat cases:
- onboard + normalize Windows + WAF telemetry
- write detections (SPL)
- add correlation + noise reduction
- document everything so another analyst can run it

## Scope (what the “client” asked for)
- Quick onboarding guidance (what to collect and how to map fields)
- 5–7 production-style detections for credential abuse and web login attacks
- At least one correlation use-case (web + Windows in one story)
- Basic automation (alert actions / dedup / allowlists)

## What I set up
### 1) Indexes and sourcetypes (simple model)
- `index=win` for Windows events
  - `sourcetype=WinEventLog:Security`
- `index=waf` for Web/WAF events
  - `sourcetype=waf:access` (can be nginx / cloudflare / any WAF-like access log)

### 2) Field normalization (practical, not perfect CIM)
I kept the mapping lightweight so it’s easy to maintain:
- **Windows**
  - `EventCode` (4625 / 4624 / 4728 / 4732)
  - `user` (mapped from `TargetUserName`)
  - `src_ip` (mapped from `IpAddress`)
  - `host` (mapped from `ComputerName`)
- **WAF/Web**
  - `src_ip`, `http_method`, `uri_path`, `status`, `user_agent`

Goal: make the detections readable and consistent across sources.

## Simulated incident story (what the detections catch)
1) A public-facing login page starts getting hammered from a few IPs.
2) WAF shows many 401/403 responses and repetitive attempts to `/login`.
3) Shortly after that, Windows logs show a burst of 4625 failures for the same usernames.
4) Then we see a successful 4624 login for a targeted user.
5) The pattern looks like **credential stuffing** + **password spraying** leading to an account compromise attempt.

## Deliverables
- Detections: `detections_spl.md`
- Automation and tuning: `automation.md`
- Test dataset + helper script:
  - `sample_events.jsonl`
  - `log_generator.py`

## How I worked (including AI)
- Used ChatGPT as a helper for:
  - drafting SPL variations (same logic, different Splunk functions)
  - brainstorming edge cases (service accounts, proxies, NAT)
  - rewriting notes into clean, client-friendly language
- Manual validation:
  - checked field availability with quick `stats` searches
  - verified each query returns the expected events from `sample_events.jsonl`
  - added throttling and allowlists to keep false positives low

## Results
- Delivered 6 SPL detections + 1 correlation pattern
- Added basic automation (dedup, throttling, allowlists, alert payload template)
- Produced a small repeatable dataset and generator to test detections fast

## Notes
This case is written like a real client delivery, but it’s simulated for portfolio purposes.
