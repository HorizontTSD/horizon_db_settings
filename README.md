<p align="center">

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![Code Coverage](coverage.svg)

</p>

# Создание`.env`

Для корректной работы проекта необходимо создать файл `.env` в корне проекта со следующими переменными окружения:

```asciidoc
TOKENS_LIST=
PUBLIC_OR_LOCAL=
SERVICE_NAME=
HOST=
PORT=
VERIFY_TOKEN=
```

| Переменная        | Обязательность | Значение по умолчанию                | Описание                                                                  |
| ----------------- | -------------- |--------------------------------------| ------------------------------------------------------------------------- |
| `TOKENS_LIST`     | Обязательно    | —                                    | Ссылка на CSV со списком токенов. CSV должен содержать `token` и `source` |
| `PUBLIC_OR_LOCAL` | Необязательно  | LOCAL                                | Режим работы (например, `public` или `local`)                             |
| `SERVICE_NAME`    | Необязательно  | Имя сервиса по умолчанию из template | Имя сервиса для работы с токенами                                         |
| `HOST`            | Необязательно  | `localhost`                          | Хост для сервиса                                                          |
| `PORT`            | Необязательно  | `7070`                               | Порт для сервиса                                                          |
| `VERIFY_TOKEN`    | Необязательно  | `True`                               | Флаг проверки токена                                                      |


для создание базы проходим шаги



# Развёртывание PostgreSQL на сервере

## 1. Установка PostgreSQL

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```
### Проверка состояния сервиса:

```bash
sudo systemctl status postgresql
```

## 2. Создание нового кластера PostgreSQL на порту 8502

```bash
sudo pg_createcluster 14 main -p 8502
sudo pg_ctlcluster 14 secondary start
sudo pg_lsclusters
```
Если кластер создан и статус online, продолжаем.

## 3. Создание базы и пользователя
Под пользователем postgres
```bash
sudo -u postgres psql
```

Внутри psql:
```bash
CREATE USER User WITH PASSWORD 'PASSWORD!';
CREATE DATABASE horizon_user_db OWNER HorizonSuperUser;
ALTER USER HorizonSuperUser WITH SUPERUSER;
\q
```

Проверка подключения:
```bash
psql -h 127.0.0.1 -p 8502 -U User -d db

```

## 4. Настройка внешнего доступа
1. Открыть конфиг кластера:
```bash
sudo nano /etc/postgresql/14/main/postgresql.conf
```
Добавить или изменить строки::
```bash
listen_addresses = '*'
port = 8502
ssl = off
```
2. Настроить pg_hba.conf:
```bash
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

Добавить в конец::
```bash
host    all             HorizonSuperUser       0.0.0.0/0            md5

```

3. Перезапустить кластер:
```bash
sudo pg_ctlcluster 14 main restart
```

## 5. Проверка внешнего подключения

```bash
psql -h <IP_сервера> -p 8502 -U HorizonSuperUser -d horizon_user_db
```