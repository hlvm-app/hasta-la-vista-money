Инструкция по установке и запуску находится в разработке...
___

# Установка и запуск приложения
___   
Запустить приложение вы можете через Poetry или Docker.   

Установить **Poetry** командой:   

**Linux, macOS, Windows (WSL):**
```bash
sudo apt install python3-poetry
```

Подробная инструкция по установке **Poetry** доступна в [официальной документации](https://python-poetry.org/docs/).

Для установки **Poetry** и приложения, потребует версия **Python 3.9+** [Официальная документация на python.org](https://www.python.org/downloads/)

Для установки **Docker**, используйте информацию в официальной документации на [docs.docker.com](https://docs.docker.com/engine/install/)

---

## 1. Установка
### 1.1 Клонирование репозитория и активация виртуального окружения

#### Клонирование репозитория:
```bash
git clone https://github.com/TurtleOld/hasta-la-vista-money.git
cd hasta-la-vista-money   
```
#### Если используете **Poetry**:
Активация виртуального окружения:
```bash
make shell
```
> Если будет ошибка: Command 'make' not found...   
> Выполните в консоли команду   
> ```bash
> sudo apt install make 
> ```
```bash
make install
```

#### Если используете **Docker**:
```bash
make docker-install
```
___

### 1.2 Заполнение значений в .env файле

Все пояснения к переменным окружения даны в [.env файле](../.env).   
Следуйте комментариям.
___

### 1.3 Завершение установки
#### Если используете **Poetry**:
```bash
make setup
```
#### Если используете **Docker**:
```bash
docker-compose run --rm django make setup
```
___

## 2. Запуск приложения для разработки

#### Если используете **Poetry**:

```
make start
```

#### Если используете **Docker**:

```
make docker-start
```
___