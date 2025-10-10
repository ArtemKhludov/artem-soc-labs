#  Case 001: Infrastructure Setup

## Цель
Настроить рабочее окружение для SOC Analyst - установить необходимые инструменты, виртуальные машины и среду для анализа.

## Задачи
- [ ] Установить Python 3.8+
- [ ] Настроить виртуальную машину (Kali Linux / Ubuntu)
- [ ] Установить базовые инструменты (Wireshark, Nmap, tcpdump)
- [ ] Настроить SIEM (опционально: Splunk Free, ELK Stack)
- [ ] Создать первый Python-скрипт для анализа логов

## Инструменты
- **VirtualBox / VMware** - для виртуальных машин
- **Python** - язык для скриптов
- **Wireshark** - анализ сетевого трафика
- **Nmap** - сканирование сетей

## Ход работы

### 1. Установка Python
```bash
python3 --version
pip3 install --upgrade pip
```

### 2. Установка виртуальной машины
- Скачать Kali Linux ISO
- Создать VM с 4GB RAM, 2 CPU, 40GB HDD
- Установить гостевые дополнения

### 3. Базовые инструменты
```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить инструменты
sudo apt install wireshark nmap tcpdump python3-pip -y
```

### 4. Первый скрипт
Создан `edr_triage.py` - анализирует EDR логи на наличие suspicious events.

## Результаты
-  Окружение настроено
-  Инструменты установлены
-  Первый скрипт работает

## Notes
**Здесь записывай наблюдения и команды**

_Пример:_
- При установке Wireshark нужны права root для захвата пакетов
- Nmap по умолчанию требует sudo для SYN scan
- Python virtual environment лучше создавать для каждого проекта

## Ссылки
- [Kali Linux Download](https://www.kali.org/get-kali/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Wireshark User Guide](https://www.wireshark.org/docs/)

---
**Дата:** 08.10.2024  
**Статус:**  Завершено

