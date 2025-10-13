# Splunk Integration Architecture Failure - Response Playbook

## Initial Assessment

### Step 1: Verify Splunk Architecture
```bash
# Check if Splunk Enterprise has outputs.conf (indicates forwarder mode)
ls -la /Applications/Splunk/etc/system/local/outputs.conf

# Check management ports
netstat -an | grep -E "(8089|8090)"

# Verify Splunk roles
/Applications/Splunk/bin/splunk status
```

### Step 2: Identify Configuration Conflicts
```bash
# Find all outputs.conf files
find /Applications/Splunk -name "outputs.conf" -type f

# Check for conflicting TCP ports
grep -r "9997\|9998" /Applications/Splunk/etc/system/local/
```

## Resolution Steps

### Step 3: Remove Forwarder Configuration from Enterprise
```bash
# Remove outputs.conf if Enterprise should be indexer-only
rm /Applications/Splunk/etc/system/local/outputs.conf

# Restart Splunk Enterprise
sudo /Applications/Splunk/bin/splunk restart
```

### Step 4: Configure Proper Port Separation
```bash
# Set different management ports
echo "mgmtHostPort = 8090" >> /Applications/SplunkForwarder/etc/system/local/server.conf

# Restart SplunkForwarder
sudo /Applications/SplunkForwarder/bin/splunk restart
```

### Step 5: Clean Up Conflicting Inputs
```bash
# Disable unnecessary app inputs
echo "disabled = true" >> /Applications/Splunk/etc/apps/audit_trail/local/inputs.conf
echo "disabled = true" >> /Applications/Splunk/etc/apps/Splunk_TA_aws/local/inputs.conf
```

## Validation

### Step 6: Test Data Flow
```bash
# Create test log entry
echo "TEST: $(date) - Validation entry" >> /tmp/test_simple.log

# Check Splunk Web interface
# Search: index=main "TEST"
```

### Step 7: Verify Clean Architecture
```bash
# Confirm no outputs.conf in Enterprise
ls /Applications/Splunk/etc/system/local/outputs.conf 2>/dev/null || echo "Clean"

# Verify port separation
netstat -an | grep -E "(8089|8090|9998)"
```

## Prevention

### Step 8: Document Architecture
- Splunk Enterprise: Indexer only (no outputs.conf)
- SplunkForwarder: Data collection only (outputs.conf to Enterprise)
- Port separation: Enterprise 8089, Forwarder 8090, Data 9998

### Step 9: Regular Monitoring
```bash
# Check for configuration drift
find /Applications/Splunk -name "outputs.conf" -newer /tmp/last_check

# Monitor data flow
tail -f /Applications/SplunkForwarder/var/log/splunk/splunkd.log | grep -i error
```
