import json

# Указываем правильный путь к файлу
with open("week1_intro/case002_triage_basics/logs_sample.json") as f:
    logs = json.load(f)

print("🔍 Analyzing logs...\n")

for log in logs:
    # Проверка на failed login
    if log.get("status") == "FAILED":
        print("🚨 SUSPICIOUS: Failed login attempt")
        print(f"   User: {log.get('user')}")
        print(f"   IP: {log.get('source_ip')}")
        print(f"   Time: {log.get('timestamp')}\n")
    
    # Проверка на PowerShell
    if "powershell" in log.get("process", "").lower():
        print("🚨 CRITICAL: PowerShell execution detected!")
        print(f"   User: {log.get('user')}")
        print(f"   Process: {log.get('process')}")
        print(f"   Time: {log.get('timestamp')}\n")
    
    # Проверка на доступ к критичным файлам
    if "/etc/shadow" in log.get("file", ""):
        print("🚨 CRITICAL: Access to sensitive file!")
        print(f"   File: {log.get('file')}")
        print(f"   User: {log.get('user')}")
        print(f"   Time: {log.get('timestamp')}\n")

print("✅ Analysis complete!")