#!/usr/bin/env python3
"""
Nmap Reconnaissance Automation Tool
Автоматизация разведки для Red Team операций
"""

import subprocess
import json
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List

class NmapRecon:
    def __init__(self, target: str):
        self.target = target
        self.results = {}
        
    def host_discovery(self, network: str = None) -> Dict:
        """Обнаружение активных хостов в сети"""
        target = network if network else self.target
        print(f"[*] Host Discovery: {target}")
        
        try:
            result = subprocess.run(
                ['nmap', '-sn', '-T4', target],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Parse active hosts
            active_hosts = []
            for line in result.stdout.split('\n'):
                if 'Nmap scan report for' in line:
                    host = line.split('for ')[-1].strip()
                    active_hosts.append(host)
            
            self.results['host_discovery'] = {
                'timestamp': datetime.now().isoformat(),
                'target_network': target,
                'active_hosts': active_hosts,
                'total_hosts': len(active_hosts)
            }
            
            print(f"[+] Found {len(active_hosts)} active hosts")
            return self.results['host_discovery']
            
        except FileNotFoundError:
            print("[!] Nmap not installed. Demo mode.")
            return self._demo_host_discovery(target)
        except Exception as e:
            print(f"[!] Error: {e}")
            return {}
    
    def port_scan_stealth(self) -> Dict:
        """Скрытное сканирование портов (SYN scan)"""
        print(f"[*] Stealth SYN scan: {self.target}")
        
        try:
            result = subprocess.run(
                ['sudo', 'nmap', '-sS', '-T2', '-p-', self.target],
                capture_output=True,
                text=True,
                timeout=1800
            )
            
            open_ports = self._parse_nmap_output(result.stdout)
            
            self.results['stealth_scan'] = {
                'timestamp': datetime.now().isoformat(),
                'target': self.target,
                'scan_type': 'SYN',
                'open_ports': open_ports
            }
            
            print(f"[+] Found {len(open_ports)} open ports")
            return self.results['stealth_scan']
            
        except FileNotFoundError:
            print("[!] Nmap not installed or sudo required. Demo mode.")
            return self._demo_stealth_scan()
        except Exception as e:
            print(f"[!] Error: {e}")
            return self._demo_stealth_scan()
    
    def service_enum(self) -> Dict:
        """Детальная идентификация сервисов"""
        print(f"[*] Service enumeration: {self.target}")
        
        try:
            result = subprocess.run(
                ['nmap', '-sV', '-sC', '--version-all', '-T3', self.target],
                capture_output=True,
                text=True,
                timeout=900
            )
            
            services = self._parse_service_info(result.stdout)
            
            self.results['service_enum'] = {
                'timestamp': datetime.now().isoformat(),
                'target': self.target,
                'services': services
            }
            
            print(f"[+] Enumerated {len(services)} services")
            return self.results['service_enum']
            
        except FileNotFoundError:
            print("[!] Nmap not installed. Demo mode.")
            return self._demo_service_enum()
        except Exception as e:
            print(f"[!] Error: {e}")
            return self._demo_service_enum()
    
    def os_detection(self) -> Dict:
        """Определение операционной системы"""
        print(f"[*] OS detection: {self.target}")
        
        try:
            result = subprocess.run(
                ['sudo', 'nmap', '-O', '--osscan-guess', self.target],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            os_info = self._parse_os_info(result.stdout)
            
            self.results['os_detection'] = {
                'timestamp': datetime.now().isoformat(),
                'target': self.target,
                'os_info': os_info
            }
            
            print(f"[+] OS detection complete")
            return self.results['os_detection']
            
        except FileNotFoundError:
            print("[!] Nmap not installed or sudo required. Demo mode.")
            return self._demo_os_detection()
        except Exception as e:
            print(f"[!] Error: {e}")
            return self._demo_os_detection()
    
    def vuln_scan_aggressive(self) -> Dict:
        """Агрессивное сканирование уязвимостей"""
        print(f"[*] Vulnerability scan: {self.target}")
        
        try:
            result = subprocess.run(
                ['nmap', '--script', 'vuln,exploit', '-T4', self.target],
                capture_output=True,
                text=True,
                timeout=1200
            )
            
            vulns = self._parse_vuln_output(result.stdout)
            
            self.results['vuln_scan'] = {
                'timestamp': datetime.now().isoformat(),
                'target': self.target,
                'vulnerabilities': vulns
            }
            
            print(f"[+] Found {len(vulns)} potential vulnerabilities")
            return self.results['vuln_scan']
            
        except FileNotFoundError:
            print("[!] Nmap not installed. Demo mode.")
            return self._demo_vuln_scan()
        except Exception as e:
            print(f"[!] Error: {e}")
            return self._demo_vuln_scan()
    
    def _parse_nmap_output(self, output: str) -> List[int]:
        """Парсинг открытых портов из вывода nmap"""
        ports = []
        for line in output.split('\n'):
            if '/tcp' in line and 'open' in line:
                port = line.split('/')[0].strip()
                if port.isdigit():
                    ports.append(int(port))
        return ports
    
    def _parse_service_info(self, output: str) -> List[Dict]:
        """Парсинг информации о сервисах"""
        services = []
        for line in output.split('\n'):
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 3:
                    services.append({
                        'port': parts[0],
                        'state': parts[1],
                        'service': parts[2] if len(parts) > 2 else 'unknown',
                        'version': ' '.join(parts[3:]) if len(parts) > 3 else ''
                    })
        return services
    
    def _parse_os_info(self, output: str) -> Dict:
        """Парсинг информации об ОС"""
        os_info = {'matches': []}
        in_os_section = False
        
        for line in output.split('\n'):
            if 'OS details:' in line:
                os_info['detected'] = line.split('OS details:')[-1].strip()
            if 'OS CPE:' in line:
                os_info['cpe'] = line.split('OS CPE:')[-1].strip()
        
        return os_info
    
    def _parse_vuln_output(self, output: str) -> List[Dict]:
        """Парсинг уязвимостей из NSE скриптов"""
        vulns = []
        current_vuln = {}
        
        for line in output.split('\n'):
            if 'VULNERABLE:' in line:
                if current_vuln:
                    vulns.append(current_vuln)
                current_vuln = {'description': line.strip()}
            elif current_vuln and ('CVE' in line or 'Risk' in line):
                current_vuln['details'] = line.strip()
        
        if current_vuln:
            vulns.append(current_vuln)
        
        return vulns
    
    # Demo mode functions
    def _demo_host_discovery(self, network: str) -> Dict:
        return {
            'timestamp': datetime.now().isoformat(),
            'target_network': network,
            'active_hosts': ['192.168.1.1', '192.168.1.10', '192.168.1.50'],
            'total_hosts': 3,
            'demo_mode': True
        }
    
    def _demo_stealth_scan(self) -> Dict:
        return {
            'timestamp': datetime.now().isoformat(),
            'target': self.target,
            'scan_type': 'SYN',
            'open_ports': [21, 22, 80, 443, 3306, 8080],
            'demo_mode': True
        }
    
    def _demo_service_enum(self) -> Dict:
        return {
            'timestamp': datetime.now().isoformat(),
            'target': self.target,
            'services': [
                {'port': '22/tcp', 'state': 'open', 'service': 'ssh', 'version': 'OpenSSH 7.9'},
                {'port': '80/tcp', 'state': 'open', 'service': 'http', 'version': 'Apache httpd 2.4.41'},
                {'port': '443/tcp', 'state': 'open', 'service': 'ssl/http', 'version': 'Apache httpd 2.4.41'},
                {'port': '3306/tcp', 'state': 'open', 'service': 'mysql', 'version': 'MySQL 5.7.30'}
            ],
            'demo_mode': True
        }
    
    def _demo_os_detection(self) -> Dict:
        return {
            'timestamp': datetime.now().isoformat(),
            'target': self.target,
            'os_info': {
                'detected': 'Linux 4.15 - 5.8',
                'cpe': 'cpe:/o:linux:linux_kernel:5.4',
                'matches': ['Ubuntu 20.04', 'Debian 10']
            },
            'demo_mode': True
        }
    
    def _demo_vuln_scan(self) -> Dict:
        return {
            'timestamp': datetime.now().isoformat(),
            'target': self.target,
            'vulnerabilities': [
                {
                    'description': 'VULNERABLE: SSL/TLS POODLE vulnerability',
                    'details': 'CVE-2014-3566 - Risk: Medium'
                },
                {
                    'description': 'VULNERABLE: MySQL weak password',
                    'details': 'Risk: High - Default credentials detected'
                }
            ],
            'demo_mode': True
        }
    
    def save_results(self, filename: str = None):
        """Сохранение результатов разведки"""
        if not filename:
            filename = f"recon_{self.target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n[+] Results saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description='Nmap Recon Automation for Red Team')
    parser.add_argument('target', help='Target IP or hostname')
    parser.add_argument('--discover', action='store_true', help='Host discovery (use with network range)')
    parser.add_argument('--stealth', action='store_true', help='Stealth SYN scan')
    parser.add_argument('--services', action='store_true', help='Service enumeration')
    parser.add_argument('--os', action='store_true', help='OS detection')
    parser.add_argument('--vuln', action='store_true', help='Vulnerability scan')
    parser.add_argument('--full', action='store_true', help='Full reconnaissance')
    parser.add_argument('--output', '-o', help='Output file')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Nmap Reconnaissance Tool - Red Team Edition")
    print("=" * 80)
    print(f"Target: {args.target}\n")
    
    recon = NmapRecon(args.target)
    
    if args.full or args.discover:
        recon.host_discovery(args.target if '/' in args.target else None)
        print()
    
    if args.full or args.stealth:
        recon.port_scan_stealth()
        print()
    
    if args.full or args.services:
        recon.service_enum()
        print()
    
    if args.full or args.os:
        recon.os_detection()
        print()
    
    if args.full or args.vuln:
        recon.vuln_scan_aggressive()
        print()
    
    if not any([args.discover, args.stealth, args.services, args.os, args.vuln, args.full]):
        print("[!] Specify reconnaissance type: --stealth, --services, --os, --vuln, or --full")
        parser.print_help()
        return
    
    if args.output:
        recon.save_results(args.output)
    else:
        recon.save_results()


if __name__ == "__main__":
    main()

