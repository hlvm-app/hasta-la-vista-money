# Вклад в проект

## Установка и запуск приложения

Запустить приложение вы можете через Poetry или Docker.

Установить **Poetry** командой:

**Linux**

``` bash
sudo apt install python3-poetry -y
```

**macOS, Windows (WSL):**

``` bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Подробная инструкция по установке **Poetry** доступна в [официальной
документации](<https://python-poetry.org/docs/>).

Для установки **Poetry** и приложения, потребует версия **Python 3.9+**
[Официальная документация на
python.org](<https://www.python.org/downloads/>)

Для установки **Docker**, используйте информацию в официальной
документации на
[docs.docker.com](<https://docs.docker.com/engine/install/>)

------------------------------------------------------------------------

## 1. Установка

#### 1.1 Клонирование репозитория и активация виртуального окружения

##### Клонирование репозитория

``` bash
git clone https://github.com/TurtleOld/hasta-la-vista-money.git
cd hasta-la-vista-money
```

##### Если используете **Poetry**

Активация виртуального окружения:

``` bash
make shell
```

Если будет ошибка: Command \'make\' not found\... Выполните в консоли
команду

``` bash
sudo apt install make
```

Затем:

``` bash
make install
```

------------------------------------------------------------------------

#### 1.2 Заполнение значений в .env файле
```bash
make .env
```

SECRET_KEY - Key for a file settings.py. You can to generation the key
on command - [make secretkey]{.title-ref}

> SECRET_KEY=

DEBUG - Activation of debugging. Do not activate on a productive server.
Specify one of three values: true, 1, yes

> DEBUG=

DATABASE_URL - URL of the connect to the database
postgres://\<username\>:\<password\>@\<name or IP
server\>:\<port\>/\<name database\>

> DATABASE_URL=

ALLOWED_HOSTS - List of allowed hosts. Example 'localhost',
'127.0.0.1'. By default, hosts - localhost, 127.0.0.1

> ALLOWED_HOSTS=

------------------------------------------------------------------------

#### 1.3 Завершение установки

##### Если используете **Poetry**

``` bash
make setup
```

##### Если используете **Docker**

``` bash
docker compose run django python manage.py migrate
docker compose run django python manage.py createsuperuser
docker compose run django python manage.py collectstatic
```

------------------------------------------------------------------------

## 2. Запуск приложения для разработки

##### Если используете **Poetry**

``` bash
make start
```

##### Если используете **Docker**

``` bash
make docker-up
```
