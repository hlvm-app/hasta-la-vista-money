# Вклад в проект

Рад видеть вас на борту! Этот раздел посвящен тому, чтобы помочь вам присоединиться к нашему проекту. Независимо от того, опытный ли вы разработчик или только начинаете, мы ценим ваш энтузиазм и готовность внести вклад. Здесь вы найдете ресурсы и руководства, которые помогут вам начать вносить вклад в наш проект.

Если у вас есть вопросы или вам нужна помощь в начале работы, не стесняйтесь спрашивать. Всегда рад сотрудничать с вами!

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

### 1.1 Клонирование репозитория и активация виртуального окружения

#### Клонирование репозитория

``` bash
git clone https://github.com/TurtleOld/hasta-la-vista-money.git
cd hasta-la-vista-money
```

### 1.2 Заполнение значений в .env файле
```bash
make .env
```
SECRET_KEY - Key for a file settings.py. You can to generation the key
on command - ```make secretkey```

> SECRET_KEY=

DEBUG - Activation of debugging. Do not activate on a productive server.
Specify one of three values: true, 1, yes

> DEBUG=

DATABASE_URL - URL of to connect to the database
postgres://username:password@name or IP server:port/name_database

> DATABASE_URL=

ALLOWED_HOSTS - List of allowed hosts. Example 'localhost',
'127.0.0.1'. By default, hosts - localhost, 127.0.0.1

> ALLOWED_HOSTS=

------------------------------------------------------------------------

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

## 2. Запуск приложения для разработки

##### Если используете **Poetry**

``` bash
make start
```

##### Если используете **Docker**

``` bash
make docker-up
```
------------------------------------------------------------------------
