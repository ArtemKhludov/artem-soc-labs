# Case-003 — Splunk Integration Architecture Failure

## Context
While integrating Splunk Enterprise, Universal Forwarder and AWS inputs, several technical issues appeared.  
The goal was to establish stable log ingestion.  
After two days of investigation, the core problem proved architectural: Splunk Enterprise operated as a forwarder instead of an indexer.

---

## Problems Investigated

### 1. Password authentication — false alarm
Multiple admin passwords (`changeme`, `admin`, custom) returned "Login failed."  
Root cause: CLI access blocked by internal misconfiguration.  
**Status:** Not a real issue.

### 2. Port conflict (8089)
Forwarder and Enterprise both bound management port 8089.  
**Fix:** Separate ports (Enterprise 8089 / Forwarder 8090).  
**Status:** Resolved.

### 3. TCP ingestion failure (9997)
Forwarder active, data absent.  
**Root cause:** Enterprise misconfigured as forwarder (`outputs.conf` present).  
**Fix:** Remove `outputs.conf` from Enterprise.  
**Status:** Resolved.

### 4. Invalid parameter `autoLB`
Unsupported key in `outputs.conf`.  
**Fix:** Delete `autoLB = true`.  
**Status:** Resolved.

### 5. File-permission errors
Forwarder lacked read rights (owner root).  
**Fix:** `chmod 644 /tmp/test_simple.log`.  
**Status:** Resolved.

### 6. macOS quarantine — false alarm
Checked `xattr`; no quarantine flags found.  
**Status:** Not a real issue.

### 7. Multiple data sources
Enterprise ingested 18 legacy inputs (AWS, attack_data, HTTP).  
**Fix:** Disabled redundant inputs, left 2 core sources.  
**Status:** Resolved.

### 8. Archived logs misread
Forwarder processed old `.gz` files as new events.  
**Fix:** Exclude archive paths from `inputs.conf`.  
**Status:** Not a real issue.

---

## Root Cause

Splunk Enterprise ran as a forwarder because of **automatic configuration created at installation**.  
The system generated `outputs.conf` by default, along with app-specific configurations that conflicted with custom settings.

---

## Detailed Cause Analysis

### Automatic configuration during install
- At install, Splunk Enterprise generates `/etc/system/default/outputs.conf`.  
- File created: **Sep 9 08:55** — same moment as base installation.  
- This file defines a forwarder role by default.

### App-level configuration
- Installed apps (`SplunkForwarder`, `audit_trail`) created their own `outputs.conf` and `inputs.conf`.  
- App timestamps: **May 12 22:23** — matched time of app setup.  
- Result: overlapping ports (9997 vs 9998) and duplicate send/receive paths.

### Why it happens
- Splunk Enterprise is designed as a hybrid node (indexer + forwarder).  
- Default install enables both roles to ensure flexibility.  
- Unless explicitly disabled, both remain active and conflict.

---

## Final Architecture

[Log Sources]
↓
[Universal Forwarder → TCP 9998]
↓
[Splunk Enterprise (Indexer)]

Validation queries:

```spl
index=* | head 10
index=main | stats count by sourcetype
```

---

## MITRE ATT&CK Mapping

| Issue | Technique ID | Tactic | Explanation |
|-------|--------------|--------|-------------|
| Misconfigured outputs / ports | T1562.001 | Defense Evasion | Visibility reduced by incorrect configuration |
| Permission errors | T1078 | Initial Access | Improper file ownership blocked collection |
| Redundant inputs | T1082 | Discovery | Noise from excessive enumeration |
| Forwarder ↔ Indexer confusion | T1070 | Defense Evasion | Logs misrouted, partial data loss |

---

## Results

| Metric | Before | After |
|--------|--------|-------|
| Active inputs | 18 (noisy) | 2 (clean) |
| Data flow | Unstable | Stable (<5 s delay) |
| TCP ports | Conflicted | Separated (8089 / 9998) |
| False alarms | 3 major | 0 active |

---

## Lessons Learned

1. Verify architecture first; credentials rarely the root cause.
2. Port conflicts usually indicate role confusion.
3. Limit data sources to essential ones to reduce noise.
4. Audit /etc/system/default — default configs override local settings.
5. Splunk Enterprise behaves as a universal server; disable unused roles after install.
