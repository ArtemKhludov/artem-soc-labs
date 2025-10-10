#!/usr/bin/env python3
"""
Directory Brute Force Tool (DirBuster Simulation)
Инструмент для обнаружения скрытых директорий и файлов на веб-серверах
"""

import requests
import argparse
import threading
from queue import Queue
from urllib.parse import urljoin
from datetime import datetime
from typing import List, Dict
import time

class DirBusterSim:
    def __init__(self, target_url: str, wordlist: str = None, threads: int = 10):
        self.target_url = target_url.rstrip('/')
        self.wordlist = wordlist
        self.threads = threads
        self.found_paths = []
        self.queue = Queue()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def load_wordlist(self) -> List[str]:
        """Загрузка wordlist для brute force"""
        if self.wordlist:
            try:
                with open(self.wordlist, 'r') as f:
                    return [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                print(f"[!] Wordlist not found: {self.wordlist}")
                return self._default_wordlist()
        else:
            return self._default_wordlist()
    
    def _default_wordlist(self) -> List[str]:
        """Дефолтный wordlist для демонстрации"""
        return [
            'admin', 'administrator', 'login', 'dashboard', 'panel',
            'wp-admin', 'phpmyadmin', 'cpanel', 'webmail',
            'backup', 'backups', '.git', '.env', 'config',
            'api', 'api/v1', 'api/v2', 'api/docs',
            'uploads', 'upload', 'files', 'images', 'assets',
            'test', 'dev', 'staging', 'beta',
            'admin.php', 'login.php', 'config.php', 'db.php',
            'robots.txt', 'sitemap.xml', '.htaccess', 'web.config',
            'swagger', 'graphql', 'wp-content', 'wp-includes',
            'vendor', 'node_modules', '.git/config', '.svn',
            'server-status', 'server-info', 'phpinfo.php',
            'shell.php', 'cmd.php', 'backdoor.php',
            'database', 'db', 'sql', 'mysql',
            'adminer.php', 'setup.php', 'install.php',
            'logs', 'log', 'error_log', 'access_log',
            'tmp', 'temp', 'cache', '.cache',
            'private', 'internal', 'secret', 'hidden',
            'user', 'users', 'account', 'profile'
        ]
    
    def check_path(self, path: str) -> Dict:
        """Проверка существования пути"""
        url = urljoin(self.target_url, path)
        
        try:
            response = self.session.get(
                url,
                timeout=5,
                allow_redirects=False,
                verify=False  # Только для тестирования!
            )
            
            result = {
                'url': url,
                'path': path,
                'status_code': response.status_code,
                'size': len(response.content),
                'found': response.status_code in [200, 201, 202, 203, 301, 302, 401, 403]
            }
            
            if result['found']:
                self.found_paths.append(result)
                status_symbol = {
                    200: '[+]',
                    301: '[>]',
                    302: '[>]',
                    401: '[!]',
                    403: '[!]'
                }.get(response.status_code, '[?]')
                
                print(f"{status_symbol} [{response.status_code}] {url} ({result['size']} bytes)")
            
            return result
            
        except requests.exceptions.Timeout:
            return {'url': url, 'error': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'url': url, 'error': 'connection_error'}
        except Exception as e:
            return {'url': url, 'error': str(e)}
    
    def worker(self):
        """Worker thread для обработки очереди"""
        while True:
            path = self.queue.get()
            if path is None:
                break
            
            self.check_path(path)
            self.queue.task_done()
            
            # Rate limiting - простая задержка
            time.sleep(0.1)
    
    def scan(self) -> List[Dict]:
        """Запуск сканирования"""
        print(f"[*] Target: {self.target_url}")
        print(f"[*] Threads: {self.threads}")
        print(f"[*] Loading wordlist...")
        
        paths = self.load_wordlist()
        print(f"[*] Loaded {len(paths)} paths to test\n")
        print("=" * 80)
        
        # Запуск worker threads
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        
        # Добавление путей в очередь
        for path in paths:
            self.queue.put(path)
        
        # Ожидание завершения
        self.queue.join()
        
        # Остановка workers
        for _ in range(self.threads):
            self.queue.put(None)
        for t in threads:
            t.join()
        
        print("=" * 80)
        print(f"\n[+] Scan complete. Found {len(self.found_paths)} interesting paths")
        
        return self.found_paths
    
    def generate_report(self) -> Dict:
        """Генерация отчета о найденных путях"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'target': self.target_url,
            'total_found': len(self.found_paths),
            'findings': {
                'critical': [],
                'high': [],
                'medium': [],
                'info': []
            }
        }
        
        # Классификация по критичности
        for finding in self.found_paths:
            path = finding['path'].lower()
            status = finding['status_code']
            
            # Критичные находки
            if any(word in path for word in ['.git', '.env', 'config.php', 'db.php', 'backup', 'shell', 'cmd']):
                report['findings']['critical'].append(finding)
            # Высокий приоритет
            elif any(word in path for word in ['admin', 'phpmyadmin', 'cpanel', 'api', 'graphql']):
                report['findings']['high'].append(finding)
            # Средний приоритет
            elif status == 403 or any(word in path for word in ['upload', 'files', 'logs']):
                report['findings']['medium'].append(finding)
            # Информационные
            else:
                report['findings']['info'].append(finding)
        
        return report
    
    def print_report(self, report: Dict):
        """Вывод отчета"""
        print("\n" + "=" * 80)
        print("DIRECTORY BRUTE FORCE REPORT")
        print("=" * 80)
        print(f"Target: {report['target']}")
        print(f"Timestamp: {report['timestamp']}")
        print(f"Total paths found: {report['total_found']}\n")
        
        for severity in ['critical', 'high', 'medium', 'info']:
            findings = report['findings'][severity]
            if findings:
                print(f"\n[{severity.upper()}] - {len(findings)} findings:")
                for finding in findings[:10]:  # Показать первые 10
                    print(f"  [{finding['status_code']}] {finding['url']}")
        
        print("\n" + "=" * 80)
    
    def save_report(self, report: Dict, filename: str = None):
        """Сохранение отчета в файл"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"dirbuster_report_{timestamp}.json"
        
        import json
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[+] Report saved to {filename}")


def main():
    # Отключение предупреждений SSL (только для тестирования!)
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    parser = argparse.ArgumentParser(description='Directory Brute Force Tool')
    parser.add_argument('url', help='Target URL (e.g., http://example.com)')
    parser.add_argument('--wordlist', '-w', help='Wordlist file path')
    parser.add_argument('--threads', '-t', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('--output', '-o', help='Output file for report (JSON)')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Directory Brute Force Tool v1.0")
    print("⚠️  For authorized testing only!")
    print("=" * 80)
    print()
    
    scanner = DirBusterSim(args.url, args.wordlist, args.threads)
    scanner.scan()
    
    report = scanner.generate_report()
    scanner.print_report(report)
    
    if args.output:
        scanner.save_report(report, args.output)
    else:
        scanner.save_report(report)


if __name__ == "__main__":
    # Example usage:
    # python dirbuster_sim.py http://testphp.vulnweb.com -t 5 --output report.json
    main()

