#  Week 1: Summary & Notes

## Основные темы
- Настройка окружения для SOC Analyst
- Первое знакомство с EDR логами
- Написание простого Python-скрипта для триажа

## Ключевые выводы

### 1. Infrastructure Setup
- Виртуальные машины - must have для безопасного тестирования
- Kali Linux содержит большинство нужных инструментов из коробки
- Python - основной язык для автоматизации SOC-задач

### 2. EDR Log Analysis
- EDR логи содержат события endpoint'ов (process creation, network connections, file modifications)
- Важно фильтровать шум и находить аномалии
- Ключевые слова: "suspicious", "alert", "malware", "ransomware"

### 3. Scripting
- Простой Python-скрипт может автоматизировать рутинные задачи
- JSON - распространенный формат для логов
- Регулярные выражения полезны для парсинга

## Команды, которые пригодились

```bash
# Проверка сетевых подключений
netstat -tulnp

# Просмотр логов аутентификации
sudo tail -f /var/log/auth.log

# Быстрый анализ подозрительных процессов
ps aux | grep -i suspicious

# Поиск в логах
grep -i "failed" /var/log/syslog
```

## Проблемы и решения

| Проблема | Решение |
|----------|---------|
| Python модули не устанавливаются | Использовать `python3 -m pip install` |
| Wireshark не захватывает пакеты | Добавить пользователя в группу `wireshark` |
| JSON файл не читается | Проверить кодировку (UTF-8) |

## Что изучить дальше
- [ ] SIEM queries (Splunk SPL, KQL)
- [ ] Threat Intelligence feeds
- [ ] Incident Response Playbooks
- [ ] MITRE ATT&CK Framework

## Notes
**Здесь записывай наблюдения и команды**

_Полезные ресурсы:_
- https://attack.mitre.org/ - MITRE ATT&CK
- https://www.sans.org/blog/ - SANS Reading Room
- https://github.com/meirwah/awesome-incident-response

---
**Week:** 1  
**Дата:** 08.10.2024  
**Часов потрачено:** ~10

