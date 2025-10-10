#!/usr/bin/env python3
"""
EDR Log Triage Script
Автоматический анализ EDR логов для поиска подозрительных событий

Author: Artem
Date: 2024-10-08
"""

import json
import sys
from datetime import datetime
from typing import List, Dict

# Ключевые слова для поиска подозрительных событий
SUSPICIOUS_KEYWORDS = [
    "suspicious", "alert", "malware", "ransomware", 
    "trojan", "exploit", "backdoor", "rootkit",
    "mimikatz", "powershell", "cmd.exe", "wscript"
]

def load_edr_logs(filepath: str) -> List[Dict]:
    """Загрузка EDR логов из JSON файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('events', [])
    except FileNotFoundError:
        print(f"[ERROR] Файл не найден: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Ошибка парсинга JSON: {e}")
        sys.exit(1)

def analyze_event(event: Dict) -> bool:
    """Проверка события на наличие подозрительных индикаторов"""
    event_str = json.dumps(event).lower()
    
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in event_str:
            return True
    return False

def triage_logs(events: List[Dict]) -> tuple:
    """Триаж логов - разделение на подозрительные и чистые"""
    suspicious = []
    clean = []
    
    for event in events:
        if analyze_event(event):
            suspicious.append(event)
        else:
            clean.append(event)
    
    return suspicious, clean

def print_summary(suspicious: List[Dict], clean: List[Dict]):
    """Вывод статистики анализа"""
    total = len(suspicious) + len(clean)
    
    print("\n" + "="*60)
    print("📊 EDR LOG TRIAGE SUMMARY")
    print("="*60)
    print(f"Total events analyzed: {total}")
    print(f"✅ Clean events: {len(clean)}")
    print(f"🚨 Suspicious events: {len(suspicious)}")
    print(f"Risk level: {'HIGH' if len(suspicious) > 5 else 'MEDIUM' if len(suspicious) > 0 else 'LOW'}")
    print("="*60 + "\n")

def print_suspicious_events(events: List[Dict]):
    """Вывод подозрительных событий"""
    if not events:
        print("✅ No suspicious events found.\n")
        return
    
    print("🚨 SUSPICIOUS EVENTS DETECTED:\n")
    
    for i, event in enumerate(events, 1):
        print(f"[{i}] Event ID: {event.get('event_id', 'N/A')}")
        print(f"    Timestamp: {event.get('timestamp', 'N/A')}")
        print(f"    Type: {event.get('event_type', 'N/A')}")
        print(f"    Process: {event.get('process_name', 'N/A')}")
        print(f"    Details: {event.get('details', 'N/A')}")
        print(f"    Severity: {event.get('severity', 'N/A')}")
        print("-" * 60)

def main():
    """Main function"""
    print("\n🛡️  EDR Log Triage Tool")
    print("=" * 60)
    
    # Путь к файлу логов
    log_file = "edr_triage_sample.json"
    
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    
    print(f"📁 Analyzing: {log_file}\n")
    
    # Загрузка и анализ
    events = load_edr_logs(log_file)
    suspicious, clean = triage_logs(events)
    
    # Вывод результатов
    print_summary(suspicious, clean)
    print_suspicious_events(suspicious)
    
    # Сохранение результатов
    if suspicious:
        output_file = f"suspicious_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(suspicious, f, indent=2, ensure_ascii=False)
        print(f"💾 Suspicious events saved to: {output_file}\n")

if __name__ == "__main__":
    main()

