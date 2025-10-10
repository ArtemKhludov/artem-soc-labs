#!/usr/bin/env python3
"""
SOC Triage Parser v2.0
Автоматический анализ логов на подозрительные события
"""

import json
import os
from datetime import datetime

def load_logs(filepath):
    """Загрузка логов из JSON файла с проверкой ошибок"""
    try:
        with open(filepath, 'r') as f:
            logs = json.load(f)
        print(f"✅ Загружено {len(logs)} событий из {filepath}\n")
        return logs
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл {filepath} не найден!")
        return []
    except json.JSONDecodeError:
        print(f"❌ Ошибка: Файл {filepath} содержит некорректный JSON!")
        return []

def analyze_failed_logins(log):
    """Анализ неудачных попыток входа"""
    if log.get("status") == "FAILED":
        return {
            "severity": "HIGH",
            "type": "Failed Login",
            "details": f"User '{log.get('user')}' from {log.get('source_ip')}",
            "timestamp": log.get("timestamp")
        }
    return None

def analyze_powershell(log):
    """Детекция PowerShell активности"""
    process = log.get("process", "").lower()
    if "powershell" in process or "pwsh" in process:
        return {
            "severity": "CRITICAL",
            "type": "PowerShell Execution",
            "details": f"User '{log.get('user')}' executed {log.get('process')}",
            "timestamp": log.get("timestamp")
        }
    return None

def analyze_sensitive_files(log):
    """Детекция доступа к критичным файлам"""
    sensitive_files = ["/etc/shadow", "/etc/passwd", "SAM", "SYSTEM", ".ssh/id_rsa"]
    file_path = log.get("file", "")
    
    for sensitive in sensitive_files:
        if sensitive in file_path:
            return {
                "severity": "CRITICAL",
                "type": "Sensitive File Access",
                "details": f"User '{log.get('user')}' accessed {file_path}",
                "timestamp": log.get("timestamp")
            }
    return None

def analyze_external_connections(log):
    """Детекция подключений с внешних IP"""
    source_ip = log.get("source_ip", "")
    
    # Проверка: не локальный IP
    if source_ip and not source_ip.startswith(("10.", "192.168.", "172.16.")):
        return {
            "severity": "MEDIUM",
            "type": "External Connection",
            "details": f"Connection from external IP: {source_ip}",
            "timestamp": log.get("timestamp")
        }
    return None

def main():
    print("=" * 80)
    print("🛡️  SOC TRIAGE PARSER v2.0")
    print("=" * 80)
    print()
    
    # Путь к файлу логов
    log_file = "logs_sample.json"
    
    # Загрузка логов
    logs = load_logs(log_file)
    if not logs:
        return
    
    # Список для хранения всех находок
    findings = []
    
    # Анализ каждого события
    for log in logs:
        # Запускаем все детекторы
        checks = [
            analyze_failed_logins(log),
            analyze_powershell(log),
            analyze_sensitive_files(log),
            analyze_external_connections(log)
        ]
        
        # Собираем все находки
        for finding in checks:
            if finding:
                findings.append(finding)
    
    # Вывод результатов
    if findings:
        print(f"🚨 Обнаружено {len(findings)} подозрительных событий:\n")
        
        # Группировка по серьезности
        critical = [f for f in findings if f['severity'] == 'CRITICAL']
        high = [f for f in findings if f['severity'] == 'HIGH']
        medium = [f for f in findings if f['severity'] == 'MEDIUM']
        
        if critical:
            print("🔴 CRITICAL:")
            for f in critical:
                print(f"   [{f['timestamp']}] {f['type']}: {f['details']}")
            print()
        
        if high:
            print("🟠 HIGH:")
            for f in high:
                print(f"   [{f['timestamp']}] {f['type']}: {f['details']}")
            print()
        
        if medium:
            print("🟡 MEDIUM:")
            for f in medium:
                print(f"   [{f['timestamp']}] {f['type']}: {f['details']}")
            print()
        
        # Рекомендации
        print("=" * 80)
        print("📋 РЕКОМЕНДАЦИИ:")
        print()
        if critical:
            print("1. 🚨 НЕМЕДЛЕННО: Изолировать скомпрометированные хосты")
            print("2. 🔒 Заблокировать подозрительные IP на firewall")
            print("3. 🔍 Провести форензик анализ затронутых систем")
        if high:
            print("4. ⏰ В течение часа: Сменить пароли пользователей")
            print("5. 📊 Проверить логи на других хостах")
        print()
        
    else:
        print("✅ Подозрительных событий не обнаружено")
    
    print("=" * 80)
    print(f"✅ Анализ завершен ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print("=" * 80)

if __name__ == "__main__":
    main()

