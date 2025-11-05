# 🚀 Splunk - Шпаргалка команд

## ⚡ Самые важные команды

### Запуск и остановка
```bash
# Запустить
sudo /Applications/Splunk/bin/splunk start

# Остановить
sudo /Applications/Splunk/bin/splunk stop

# Перезапустить
sudo /Applications/Splunk/bin/splunk restart

# Статус
sudo /Applications/Splunk/bin/splunk status
```

### Доступ к интерфейсу
```bash
# Открыть в браузере
open http://localhost:8000

# URL для доступа
http://localhost:8000
```

### Проверка
```bash
# Работает ли Splunk?
sudo /Applications/Splunk/bin/splunk status

# Какие процессы запущены?
ps aux | grep splunk | grep -v grep

# Какие порты заняты?
lsof -i :8000
```

### Автозапуск
```bash
# Включить
sudo /Applications/Splunk/bin/splunk enable boot-start

# Отключить
sudo /Applications/Splunk/bin/splunk disable boot-start
```

### Логи
```bash
# Основной лог
tail -f /Applications/Splunk/var/log/splunk/splunkd.log

# Последние 50 строк
tail -50 /Applications/Splunk/var/log/splunk/splunkd.log
```

---

## 📝 Алиасы для .zshrc (опционально)

Добавьте в `~/.zshrc` для удобства:

```bash
# Splunk алиасы
alias splunk-start='sudo /Applications/Splunk/bin/splunk start'
alias splunk-stop='sudo /Applications/Splunk/bin/splunk stop'
alias splunk-restart='sudo /Applications/Splunk/bin/splunk restart'
alias splunk-status='sudo /Applications/Splunk/bin/splunk status'
alias splunk-open='open http://localhost:8000'
alias splunk-logs='tail -f /Applications/Splunk/var/log/splunk/splunkd.log'
```

После добавления выполните:
```bash
source ~/.zshrc
```

Теперь можно использовать короткие команды:
```bash
splunk-start     # Запустить
splunk-status    # Проверить
splunk-open      # Открыть в браузере
```

---

## 🎯 Как просить Cursor помочь

**Простым языком:**
- "Запусти Splunk"
- "Проверь Splunk"
- "Останови Splunk"
- "Открой Splunk в браузере"
- "Покажи логи Splunk"
- "Splunk не работает, помоги"

**Cursor всё сделает за вас!** 🤖✨


