#  Security Glossary

Словарь терминов кибербезопасности, SOC и Red Team.


## A-E

### EDR (Endpoint Detection and Response)
**Определение:** Система обнаружения и реагирования на угрозы на конечных точках (workstations, servers).  
**Примеры:** CrowdStrike Falcon, SentinelOne, Microsoft Defender for Endpoint.  
**Применение:** Мониторинг процессов, сетевых соединений, изменений файлов; автоматическое реагирование на инциденты.

### SIEM (Security Information and Event Management)
**Определение:** Система управления информацией и событиями безопасности. Централизованный сбор, корреляция и анализ логов.  
**Примеры:** Splunk, IBM QRadar, Elastic SIEM.  
**Применение:** Обнаружение аномалий, compliance reporting, incident investigation.

### RCA (Root Cause Analysis)
**Определение:** Анализ первопричины инцидента.  
**Цель:** Понять, как произошла компрометация, чтобы предотвратить повторение.  
**Методы:** Timeline analysis, log correlation, malware reverse engineering.

### IOC (Indicator of Compromise)
**Определение:** Индикаторы компрометации - артефакты, указывающие на потенциальное вторжение.  
**Примеры:** Malicious IP addresses, file hashes, domain names, registry keys.  
**Использование:** Threat hunting, SIEM rules, blocklists.

### Playbook
**Определение:** Пошаговая инструкция для реагирования на определенный тип инцидента.  
**Примеры:** Ransomware playbook, Phishing playbook, DDoS playbook.  
**Структура:** Detection -> Analysis -> Containment -> Eradication -> Recovery.


## F-J

### SOAR (Security Orchestration, Automation and Response)
**Определение:** Платформа для автоматизации процессов реагирования на инциденты.  
**Примеры:** Palo Alto Cortex XSOAR, Splunk Phantom, IBM Resilient.  
**Возможности:** Автоматический сбор IOC, обогащение данных, координация действий команды.

### TTP (Tactics, Techniques, and Procedures)
**Определение:** Тактики, техники и процедуры, используемые атакующими.  
**Фреймворк:** MITRE ATT&CK - каталогизация всех известных TTP.  
**Применение:** Threat modeling, detection engineering, red team planning.

### C2 (Command and Control)
**Определение:** Сервер управления, через который атакующий контролирует скомпрометированные системы.  
**Протоколы:** HTTP/HTTPS, DNS, ICMP, custom protocols.  
**Обнаружение:** Network traffic analysis, anomaly detection, известные IOC.

### Lateral Movement
**Определение:** Перемещение атакующего внутри скомпрометированной сети между системами.  
**Техники:** Pass-the-Hash, RDP, PsExec, WMI, PowerShell remoting.  
**Защита:** Network segmentation, least privilege, MFA.

### Threat Intelligence (TI)
**Определение:** Информация об актуальных угрозах, актерах, их методах и индикаторах.  
**Типы:** Strategic, Tactical, Operational, Technical.  
**Источники:** OSINT, commercial feeds, ISACs, threat reports.


## K-O

### MITRE ATT&CK
**Определение:** База знаний о тактиках и техниках атакующих.  
**Структура:** 14 тактик (Initial Access, Execution, Persistence, etc.), сотни техник.  
**Применение:** Threat modeling, detection coverage mapping, red team planning.

### Zero Trust
**Определение:** Модель безопасности "никому не доверяй, всегда проверяй".  
**Принципы:** Verify explicitly, least privilege access, assume breach.  
**Реализация:** MFA, microsegmentation, continuous monitoring.

### OSINT (Open Source Intelligence)
**Определение:** Разведка из открытых источников.  
**Источники:** Social media, public databases, websites, DNS records.  
**Инструменты:** theHarvester, Shodan, Maltego, Google dorking.


## P-T

### Persistence
**Определение:** Закрепление атакующего в системе для сохранения доступа.  
**Методы:** Registry Run keys, Scheduled Tasks, Services, WMI subscriptions.  
**Обнаружение:** Autoruns analysis, baseline comparison, SIEM alerts.

### Privilege Escalation
**Определение:** Повышение привилегий из обычного пользователя до администратора/SYSTEM.  
**Техники:** Exploit vulnerabilities, misconfigured services, token manipulation.  
**Защита:** Patch management, least privilege, UAC, EDR.

### Threat Hunting
**Определение:** Проактивный поиск угроз в сети (hypothesis-driven).  
**Подход:** Формулирование гипотез  сбор данных  анализ  подтверждение/опровержение.  
**Инструменты:** SIEM, EDR, network traffic analysis, threat intelligence.


## U-Z

### Kill Chain
**Определение:** Модель стадий кибератаки (Lockheed Martin Cyber Kill Chain).  
**Стадии:** Reconnaissance  Weaponization  Delivery  Exploitation  Installation  C2  Actions on Objectives.  
**Применение:** Понимание, на какой стадии прервать атаку.

### WAF (Web Application Firewall)
**Определение:** Firewall для защиты веб-приложений от атак.  
**Защита от:** SQL injection, XSS, CSRF, DDoS.  
**Примеры:** Cloudflare WAF, AWS WAF, ModSecurity.

### Purple Team
**Определение:** Совместная работа Red Team (атакующих) и Blue Team (защитников).  
**Цель:** Улучшение detection capabilities через симуляцию реальных атак.  
**Результат:** Улучшенные playbooks, tuned SIEM rules, trained analysts.


## Аббревиатуры

- **APT** - Advanced Persistent Threat
- **C&C / C2** - Command and Control
- **CVE** - Common Vulnerabilities and Exposures
- **DLP** - Data Loss Prevention
- **IDS/IPS** - Intrusion Detection/Prevention System
- **IR** - Incident Response
- **MFA** - Multi-Factor Authentication
- **NGFW** - Next-Generation Firewall
- **OWASP** - Open Web Application Security Project
- **RCE** - Remote Code Execution
- **SOC** - Security Operations Center
- **STIG** - Security Technical Implementation Guide
- **TTPs** - Tactics, Techniques, and Procedures
- **UAC** - User Account Control
- **UEBA** - User and Entity Behavior Analytics
- **XDR** - Extended Detection and Response


**Last reviewed:** Oct 2025  
**Источники:** MITRE, NIST, SANS, личный опыт

