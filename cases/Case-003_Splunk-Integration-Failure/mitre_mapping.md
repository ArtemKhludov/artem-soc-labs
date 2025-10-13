# MITRE ATT&CK Mapping - Splunk Integration Failure

## Overview
This case demonstrates how misconfigured SIEM infrastructure can lead to reduced visibility and potential security gaps, mapping to several MITRE ATT&CK techniques.

## Technique Mappings

### T1562.001 - Impair Defenses: Disable or Modify Tools
**Tactic:** Defense Evasion  
**Description:** Adversaries may disable or modify security tools to avoid detection.

**Connection to Case:**
- Splunk Enterprise misconfigured as forwarder instead of indexer
- `outputs.conf` present in Enterprise reduced visibility into log data
- Data flow disruption created blind spots in monitoring

**Indicators:**
- Missing or delayed log ingestion
- Splunk Enterprise attempting to forward data instead of indexing
- Port conflicts between forwarder and indexer roles

### T1078 - Valid Accounts
**Tactic:** Initial Access  
**Description:** Adversaries may obtain and abuse credentials of existing accounts.

**Connection to Case:**
- File permission errors prevented SplunkForwarder from reading log files
- Root ownership of test files blocked data collection
- Improper file permissions created gaps in log monitoring

**Indicators:**
- Permission denied errors in SplunkForwarder logs
- Files owned by root when SplunkForwarder runs as splunk user
- Missing log entries in Splunk interface

### T1082 - System Information Discovery
**Tactic:** Discovery  
**Description:** Adversaries may attempt to get a listing of system information.

**Connection to Case:**
- Multiple redundant data sources (18 active inputs) created noise
- AWS S3 monitoring, attack_data directories, HTTP inputs generated excessive data
- Information overload reduced ability to identify real threats

**Indicators:**
- High volume of irrelevant log entries
- Multiple overlapping data sources
- Difficulty identifying genuine security events

### T1070 - Indicator Removal on Host
**Tactic:** Defense Evasion  
**Description:** Adversaries may delete or modify artifacts generated within systems.

**Connection to Case:**
- Logs misrouted due to forwarder/indexer confusion
- Partial data loss from conflicting configurations
- Archived logs processed as new events, obscuring timeline

**Indicators:**
- Logs appearing in wrong indexes
- Duplicate or misrouted log entries
- Inconsistent timestamping of events

## Detection Recommendations

### For T1562.001 (Tool Modification)
```spl
index=_internal source="*splunkd.log" "outputs.conf" OR "forwarder" OR "indexer"
```

### For T1078 (Permission Issues)
```spl
index=_internal source="*splunkd.log" "permission denied" OR "access denied"
```

### For T1082 (Information Discovery)
```spl
index=main | stats count by sourcetype | where count > 1000
```

### For T1070 (Log Manipulation)
```spl
index=main | eval time_diff = _time - strptime(timestamp, "%Y-%m-%d %H:%M:%S") | where time_diff > 3600
```

## Mitigation Strategies

1. **Regular Architecture Audits**
   - Verify Splunk roles and configurations monthly
   - Check for unexpected outputs.conf files
   - Validate port assignments and data flow

2. **Permission Management**
   - Implement least-privilege access for SplunkForwarder
   - Regular file ownership audits
   - Automated permission validation scripts

3. **Data Source Optimization**
   - Limit inputs to essential sources only
   - Regular cleanup of redundant configurations
   - Monitor for unusual data volume spikes

4. **Configuration Drift Prevention**
   - Version control for Splunk configurations
   - Automated configuration validation
   - Alert on unexpected configuration changes
