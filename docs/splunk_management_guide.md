# 🔍 Руководство по управлению Splunk на Mac

## 📋 Содержание
1. [Основные команды](#основные-команды)
2. [Запуск и остановка](#запуск-и-остановка)
3. [Проверка статуса](#проверка-статуса)
4. [Доступ к веб-интерфейсу](#доступ-к-веб-интерфейсу)
5. [Автозапуск](#автозапуск)
6. [Полезные команды](#полезные-команды)
7. [Решение проблем](#решение-проблем)

---

## 🎯 Основные команды

### Где находится Splunk
```bash
# Путь к установке Splunk
/Applications/Splunk

# Путь к исполняемому файлу
/Applications/Splunk/bin/splunk
```

### Базовая структура команды
```bash
sudo /Applications/Splunk/bin/splunk [команда] [параметры]
```

> ⚠️ **Важно:** Большинство команд требуют `sudo` (права администратора)

---

## 🚀 Запуск и остановка

### 1. Запустить Splunk
```bash
sudo /Applications/Splunk/bin/splunk start
```

**С автоматическим принятием лицензии (первый запуск):**
```bash
sudo /Applications/Splunk/bin/splunk start --accept-license --answer-yes
```

### 2. Остановить Splunk
```bash
sudo /Applications/Splunk/bin/splunk stop
```

### 3. Перезапустить Splunk
```bash
sudo /Applications/Splunk/bin/splunk restart
```

---

## 🔍 Проверка статуса

### Проверить, работает ли Splunk
```bash
sudo /Applications/Splunk/bin/splunk status
```

**Что вы увидите:**
- ✅ `splunkd is running (PID: xxxx)` - работает
- ❌ `splunkd was not running` - не запущен

### Проверить какие порты использует
```bash
lsof -i :8000  # Web интерфейс
lsof -i :8089  # Management порт
lsof -i :8191  # KV Store
```

### Проверить процессы Splunk
```bash
ps aux | grep splunk | grep -v grep
```

---

## 🌐 Доступ к веб-интерфейсу

### URL для доступа
```
http://localhost:8000
http://127.0.0.1:8000
http://Mac.lan:8000
```

### Открыть Splunk в браузере из терминала
```bash
open http://localhost:8000
```

### Порты Splunk
- **8000** - Web UI (основной интерфейс)
- **8089** - Management API
- **8065** - AppServer
- **8191** - KV Store

---

## ⚙️ Автозапуск

### Включить автозапуск при загрузке Mac
```bash
sudo /Applications/Splunk/bin/splunk enable boot-start
```

### Отключить автозапуск
```bash
sudo /Applications/Splunk/bin/splunk disable boot-start
```

### Проверить статус автозапуска
```bash
sudo /Applications/Splunk/bin/splunk status
```

---

## 🔧 Полезные команды

### Показать версию Splunk
```bash
/Applications/Splunk/bin/splunk version
```

### Показать путь установки
```bash
/Applications/Splunk/bin/splunk show splunkd-port
```

### Показать текущего пользователя
```bash
/Applications/Splunk/bin/splunk show user
```

### Сменить пароль администратора
```bash
sudo /Applications/Splunk/bin/splunk edit user admin -password НОВЫЙ_ПАРОЛЬ -auth admin:СТАРЫЙ_ПАРОЛЬ
```

### Показать все индексы
```bash
/Applications/Splunk/bin/splunk list index
```

### Просмотр логов Splunk
```bash
# Основной лог
tail -f /Applications/Splunk/var/log/splunk/splunkd.log

# Веб-сервер
tail -f /Applications/Splunk/var/log/splunk/web_service.log

# Ошибки
tail -f /Applications/Splunk/var/log/splunk/splunkd_stderr.log
```

---

## 🛠️ Решение проблем

### Проблема: "Permission denied"
**Решение:** Используйте `sudo` перед командой
```bash
sudo /Applications/Splunk/bin/splunk status
```

### Проблема: "Port 8000 already in use"
**Решение 1:** Найти и остановить процесс на порту 8000
```bash
# Найти процесс
lsof -i :8000

# Убить процесс (замените PID на реальный)
sudo kill -9 PID
```

**Решение 2:** Изменить порт Splunk
```bash
sudo /Applications/Splunk/bin/splunk set web-port 8001
sudo /Applications/Splunk/bin/splunk restart
```

### Проблема: Splunk не запускается
**Шаг 1:** Проверьте логи
```bash
tail -100 /Applications/Splunk/var/log/splunk/splunkd.log
```

**Шаг 2:** Очистите старые PID файлы
```bash
sudo rm -f /Applications/Splunk/var/run/splunk/splunkd.pid
sudo /Applications/Splunk/bin/splunk start
```

**Шаг 3:** Проверьте права доступа
```bash
sudo chown -R $(whoami):staff /Applications/Splunk/var/
```

### Проблема: Забыли пароль администратора
**Решение:** Сброс пароля
```bash
# Остановить Splunk
sudo /Applications/Splunk/bin/splunk stop

# Удалить файл паролей
sudo rm /Applications/Splunk/etc/passwd

# Запустить Splunk (создаст нового пользователя)
sudo /Applications/Splunk/bin/splunk start
```

---

## 📊 Быстрые команды (для копирования)

### Проверка и запуск (одна команда)
```bash
sudo /Applications/Splunk/bin/splunk status || sudo /Applications/Splunk/bin/splunk start
```

### Полный перезапуск с проверкой
```bash
echo "Останавливаю Splunk..." && \
sudo /Applications/Splunk/bin/splunk stop && \
sleep 3 && \
echo "Запускаю Splunk..." && \
sudo /Applications/Splunk/bin/splunk start && \
echo "Проверяю статус..." && \
sudo /Applications/Splunk/bin/splunk status
```

### Открыть Splunk в браузере
```bash
sudo /Applications/Splunk/bin/splunk status > /dev/null 2>&1 && \
echo "Splunk работает" && open http://localhost:8000 || \
echo "Splunk не запущен, запускаю..." && sudo /Applications/Splunk/bin/splunk start && open http://localhost:8000
```

---

## 🎓 Как работать с Cursor AI

### 1. Попросить запустить Splunk
```
"Запусти Splunk"
"Включи Splunk веб-интерфейс"
```

### 2. Проверить статус
```
"Проверь работает ли Splunk"
"Покажи статус Splunk"
```

### 3. Остановить
```
"Останови Splunk"
"Выключи Splunk"
```

### 4. Решить проблему
```
"Splunk не запускается, помоги"
"Порт 8000 занят, что делать?"
```

### 5. Настроить
```
"Включи автозапуск Splunk"
"Смени порт Splunk на 8001"
```

---

## 💡 Полезные ссылки

- **Документация Splunk:** https://docs.splunk.com
- **Splunk Answers:** https://community.splunk.com
- **Конфиг файлы:** `/Applications/Splunk/etc/system/local/`
- **Индексы:** `/Applications/Splunk/var/lib/splunk/`
- **Логи:** `/Applications/Splunk/var/log/splunk/`

---

## ✅ Чек-лист базовой работы

- [x] Знаю как запустить Splunk
- [x] Знаю как остановить Splunk  
- [x] Знаю как проверить статус
- [x] Могу открыть веб-интерфейс
- [ ] Знаю где находятся логи
- [ ] Могу решить базовые проблемы
- [ ] Настроил автозапуск (опционально)

---

**Создано:** $(date +"%Y-%m-%d")  
**Автор:** Artem  
**Проект:** artem-soc-labs


