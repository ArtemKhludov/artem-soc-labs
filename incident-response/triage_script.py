#!/usr/bin/env python3
"""
Incident Response Triage Automation Script
Автоматизация первичного анализа инцидента согласно NIST framework
"""

import os
import re
import json
import argparse
from datetime import datetime
from collections import defaultdict
from typing import Dict, List

class IRTriageAnalyzer:
    def __init__(self, log_dir: str = "./logs"):
        self.log_dir = log_dir
        self.findings = defaultdict(list)
        
    def analyze_auth_log(self, filepath: str) -> Dict:
        """Анализ файла auth.log на подозрительную активность"""
        print(f"[*] Анализ {filepath}...")
        
        if not os.path.exists(filepath):
            print(f"[!] Файл не найден: {filepath}")
            return {}
        
        failed_logins = defaultdict(int)
        successful_logins = []
        sudo_activities = []
        ssh_connections = []
        
        with open(filepath, 'r', errors='ignore') as f:
            for line in f:
                # Failed password attempts
                if 'Failed password' in line:
                    match = re.search(r'for (\w+) from ([\d\.]+)', line)
                    if match:
                        user, ip = match.groups()
                        failed_logins[f"{user}@{ip}"] += 1
                
                # Successful logins
                if 'Accepted password' in line or 'Accepted publickey' in line:
                    match = re.search(r'for (\w+) from ([\d\.]+)', line)
                    if match:
                        successful_logins.append({
                            'timestamp': line[:15],
                            'user': match.group(1),
                            'ip': match.group(2),
                            'method': 'password' if 'password' in line else 'publickey'
                        })
                
                # Sudo commands
                if 'sudo:' in line and 'COMMAND=' in line:
                    match = re.search(r'(\w+) : COMMAND=(.+)', line)
                    if match:
                        sudo_activities.append({
                            'timestamp': line[:15],
                            'user': match.group(1),
                            'command': match.group(2).strip()
                        })
                
                # SSH connections
                if 'sshd' in line and 'Connection from' in line:
                    match = re.search(r'from ([\d\.]+)', line)
                    if match:
                        ssh_connections.append({
                            'timestamp': line[:15],
                            'ip': match.group(1)
                        })
        
        # Detect brute force attempts (>5 failed attempts)
        brute_force_candidates = {k: v for k, v in failed_logins.items() if v > 5}
        
        if brute_force_candidates:
            self.findings['CRITICAL'].append({
                'type': 'Brute Force Attack Detected',
                'details': brute_force_candidates,
                'source': 'auth.log'
            })
        
        if failed_logins:
            self.findings['WARNING'].append({
                'type': 'Failed Login Attempts',
                'count': len(failed_logins),
                'details': dict(list(failed_logins.items())[:10]),
                'source': 'auth.log'
            })
        
        return {
            'failed_logins': dict(failed_logins),
            'successful_logins': successful_logins[-10:],  # Last 10
            'sudo_activities': sudo_activities[-10:],
            'ssh_connections': ssh_connections[-10:],
            'brute_force_detected': len(brute_force_candidates) > 0
        }
    
    def analyze_syslog(self, filepath: str) -> Dict:
        """Анализ syslog на аномалии и ошибки"""
        print(f"[*] Анализ {filepath}...")
        
        if not os.path.exists(filepath):
            print(f"[!] Файл не найден: {filepath}")
            return {}
        
        errors = []
        warnings = []
        kernel_messages = []
        network_events = []
        
        with open(filepath, 'r', errors='ignore') as f:
            for line in f:
                # Критические ошибки
                if 'error' in line.lower() or 'critical' in line.lower():
                    errors.append({
                        'timestamp': line[:15],
                        'message': line.strip()
                    })
                
                # Предупреждения
                if 'warning' in line.lower():
                    warnings.append({
                        'timestamp': line[:15],
                        'message': line.strip()
                    })
                
                # Kernel messages
                if 'kernel:' in line:
                    kernel_messages.append({
                        'timestamp': line[:15],
                        'message': line.strip()
                    })
                
                # Network events
                if any(net in line.lower() for net in ['network', 'dhcp', 'firewall', 'iptables']):
                    network_events.append({
                        'timestamp': line[:15],
                        'message': line.strip()
                    })
        
        if len(errors) > 10:
            self.findings['HIGH'].append({
                'type': 'Multiple System Errors',
                'count': len(errors),
                'sample': errors[:5],
                'source': 'syslog'
            })
        
        if len(kernel_messages) > 20:
            self.findings['MEDIUM'].append({
                'type': 'Kernel Activity Spike',
                'count': len(kernel_messages),
                'source': 'syslog'
            })
        
        return {
            'total_errors': len(errors),
            'total_warnings': len(warnings),
            'kernel_messages': len(kernel_messages),
            'network_events': network_events[-10:],
            'recent_errors': errors[-10:]
        }
    
    def check_indicators_of_compromise(self) -> List[Dict]:
        """Проверка индикаторов компрометации (IOC)"""
        iocs = []
        
        # Check for common malicious IPs (пример)
        malicious_ips = ['45.142.212.61', '185.220.101.', '192.168.100.']
        
        for finding_level, findings in self.findings.items():
            for finding in findings:
                if 'details' in finding:
                    details_str = str(finding['details'])
                    for malicious_ip in malicious_ips:
                        if malicious_ip in details_str:
                            iocs.append({
                                'type': 'Known Malicious IP',
                                'ip': malicious_ip,
                                'context': finding['type']
                            })
        
        if iocs:
            self.findings['CRITICAL'].extend(iocs)
        
        return iocs
    
    def generate_triage_report(self) -> Dict:
        """Генерация отчета по результатам triage"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'incident_severity': self._calculate_severity(),
            'findings': dict(self.findings),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _calculate_severity(self) -> str:
        """Расчет общей серьезности инцидента"""
        if self.findings.get('CRITICAL'):
            return 'CRITICAL'
        elif self.findings.get('HIGH'):
            return 'HIGH'
        elif self.findings.get('MEDIUM'):
            return 'MEDIUM'
        elif self.findings.get('WARNING'):
            return 'LOW'
        else:
            return 'INFO'
    
    def _generate_recommendations(self) -> List[str]:
        """Генерация рекомендаций на основе находок"""
        recommendations = []
        
        if self.findings.get('CRITICAL'):
            recommendations.append("НЕМЕДЛЕННО: Изолировать скомпрометированные системы")
            recommendations.append("Активировать Incident Response команду")
            recommendations.append("Начать сбор форензик данных")
        
        if any('Brute Force' in str(f) for f in self.findings.get('CRITICAL', [])):
            recommendations.append("Заблокировать IP-адреса источников brute force атак")
            recommendations.append("Усилить политику паролей")
            recommendations.append("Внедрить rate limiting для SSH")
        
        if self.findings.get('HIGH'):
            recommendations.append("Провести детальное расследование всех HIGH findings")
            recommendations.append("Обновить правила SIEM для детекции подобных событий")
        
        if not recommendations:
            recommendations.append("Продолжить мониторинг системы")
            recommendations.append("Задокументировать результаты анализа")
        
        return recommendations
    
    def print_report(self, report: Dict):
        """Вывод отчета в консоль"""
        print("\n" + "=" * 80)
        print("INCIDENT RESPONSE TRIAGE REPORT")
        print("=" * 80)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Incident Severity: {report['incident_severity']}\n")
        
        print("FINDINGS:")
        print("-" * 80)
        for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'WARNING', 'INFO']:
            if level in report['findings'] and report['findings'][level]:
                print(f"\n[{level}]")
                for finding in report['findings'][level]:
                    print(f"  - {finding.get('type', 'Unknown')}")
                    if 'count' in finding:
                        print(f"    Count: {finding['count']}")
                    if 'source' in finding:
                        print(f"    Source: {finding['source']}")
        
        print("\n" + "-" * 80)
        print("RECOMMENDATIONS:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(description='IR Triage Automation Script')
    parser.add_argument('--log-dir', default='./logs', help='Directory containing log files')
    parser.add_argument('--output', '-o', help='Output file for JSON report')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Incident Response Triage Analyzer v1.0")
    print("=" * 80)
    
    analyzer = IRTriageAnalyzer(args.log_dir)
    
    # Analyze logs
    auth_log = os.path.join(args.log_dir, 'auth.log')
    syslog = os.path.join(args.log_dir, 'syslog')
    
    analyzer.analyze_auth_log(auth_log)
    analyzer.analyze_syslog(syslog)
    analyzer.check_indicators_of_compromise()
    
    # Generate report
    report = analyzer.generate_triage_report()
    analyzer.print_report(report)
    
    # Save to file if specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n[+] Report saved to {args.output}")
    
    print("\n[+] Triage analysis complete")


if __name__ == "__main__":
    main()

