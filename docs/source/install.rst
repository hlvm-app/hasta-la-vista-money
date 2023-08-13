Вклад в проект
**************

Установка и запуск приложения
-----------------------------
Запустить приложение вы можете через Poetry или Docker.

Установить **Poetry** командой:

**Linux**

.. code-block:: bash

    sudo apt install python3-poetry -y

**macOS, Windows (WSL):**

.. code:: bash

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

|

Подробная инструкция по установке **Poetry** доступна в [официальной документации](https://python-poetry.org/docs/).

Для установки **Poetry** и приложения, потребует версия **Python 3.9+** [Официальная документация на python.org](https://www.python.org/downloads/)

Для установки **Docker**, используйте информацию в официальной документации на [docs.docker.com](https://docs.docker.com/engine/install/)

----------

1. Установка
------------
1.1 Клонирование репозитория и активация виртуального окружения
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
|

Клонирование репозитория
########################
.. code:: bash

    git clone https://github.com/TurtleOld/hasta-la-vista-money.git
    cd hasta-la-vista-money

|

Если используете **Poetry**
###########################

Активация виртуального окружения:

.. code:: bash

    make shell

Если будет ошибка: Command 'make' not found...
Выполните в консоли команду

.. code:: bash

    sudo apt install make

Затем:

.. code:: bash

    make install

|

Если используете **Docker**
###########################
.. code:: bash

    make docker-install

----------

1.2 Заполнение значений в .env файле
'''''''''''''''''''''''''''''''''''''

SECRET_KEY - Key for a file settings.py.
You can to generation the key on command - `make secretkey`

    SECRET_KEY=

DEBUG - Activation of debugging. Do not activate on a productive server.
Specify one of three values: true, 1, yes

    DEBUG=

TOKEN_TELEGRAM_BOT - Token for a telegram bot.

    TOKEN_TELEGRAM_BOT=

DATABASE_URL - URL of the connect to the database postgres://<username>:<password>@<name or IP server>:<port>/<name database>

    DATABASE_URL=

ACCESS_TOKEN - Token RollBar a service for tracking and collecting errors of web and mobile applications,
notifies the developer and analyzes them in order to make it easier to debug and fix bugs.

    ACCESS_TOKEN=

ID_GROUP_USER - ID of the group telegram or personal ID for error notification

    ID_GROUP_USER=

ALLOWED_HOSTS - List of allowed hosts. Example 'localhost', '127.0.0.1'.
By default hosts - localhost, 127.0.0.1

    ALLOWED_HOSTS=

-----------------

1.3 Завершение установки
''''''''''''''''''''''''
|

Если используете **Poetry**
###########################
.. code:: bash

    make setup

|

Если используете **Docker**
###########################

.. code:: bash

    docker compose run django python manage.py migrate
    docker compose run django python manage.py createsuperuser
    docker compose run django python manage.py collectstatic

----------------


2. Запуск приложения для разработки
'''''''''''''''''''''''''''''''''''
|

Если используете **Poetry**
###########################

.. code:: bash

    make start

|

Если используете **Docker**
###########################

.. code:: bash

   make docker-start
