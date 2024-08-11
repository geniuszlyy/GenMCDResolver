# GenMCDResolver
is a powerful and user-friendly domain resolver designed for identifying Minecraft server domains. It features multi-threading for fast IP resolution and special handling for Cloudflare IP ranges. 

# EN
**GenMCDResolver** is a modern domain resolver specifically designed for identifying Minecraft server domains. It features a user-friendly command-line interface and leverages multi-threading for efficient IP address resolution. The tool also includes special handling for Cloudflare IP ranges to help distinguish between server IPs and Cloudflare's protective network.

## Features
- Resolves domain names to IP addresses
- Identifies Cloudflare-protected domains
- Supports multi-threading for faster processing
- Outputs results in real-time with color-coded statuses
- Option to save results to a file

## Usage

### Command Line Options
```bash
python GenMCDResolver.py -> Displays both unique and already-found IP addresses
python GenMCDResolver.py --unique -> Displays only unique IP addresses
```

![image](https://github.com/user-attachments/assets/59007e21-f602-43b5-9cd4-5473fc3dabda)

## How to Run
1. **Clone the repository**:
```bash
git clone https://github.com/geniuszlyy/GenMCDResolver.git
```
2. **Navigate to the project directory**:
```bash
cd GenMCDResolver
```
3. **Install the required dependencies**:
```bash
pip install -r requirements.txt
```
4. **Run the program**:
```bash
python GenMCDResolver.py
```

## Examples
To resolve domains from a list, simply run the script and follow the prompts:
```bash
python GenMCDResolver.py
```
You'll be prompted to enter the domain, subdomain list, top-level domain list, and the number of threads to use.

![image](https://github.com/user-attachments/assets/3589eafa-76a8-4887-8772-3118b249a3a9)

![image](https://github.com/user-attachments/assets/a023353c-a86f-4d55-8a3c-55ef537743e4)

# RU
**GenMCDResolver** - это современный резольвер доменов, специально разработанный для определения доменов серверов Minecraft. Он имеет удобный интерфейс командной строки и использует многопоточность для эффективного разрешения IP-адресов. В инструмент также включена специальная обработка IP-диапазонов Cloudflare для различения IP-адресов серверов и защитной сети Cloudflare.

## Особенности
- Разрешает доменные имена в IP-адреса
- Идентифицирует домены, защищенные Cloudflare
- Поддержка многопоточности для быстрого обработки
- Выводит результаты в реальном времени с цветовой кодировкой статусов
- Возможность сохранения результатов в файл

## Использование
### Параметры командной строки
```bash
python GenMCDResolver.py -> Показывает как уникальные, так и уже найденные IP-адреса
python GenMCDResolver.py --unique -> Показывает только уникальные IP-адреса
```

![image](https://github.com/user-attachments/assets/59007e21-f602-43b5-9cd4-5473fc3dabda)

## Как запустить
1. **Клонируйте репозиторий**:
```bash
git clone https://github.com/geniuszlyy/GenMCDResolver.git
```
2. **Перейдите в каталог проекта**:
```bash
cd GenMCDResolver
```
3. **Установите необходимые зависимости**:
```bash
pip install -r requirements.txt
```
4. **Запустите программу**:
```bash
python GenMCDResolver.py
```

## Примеры
Для разрешения доменов из списка просто запустите скрипт и следуйте инструкциям:
```bash
python GenMCDResolver.py
```
Вам будет предложено ввести домен, список поддоменов, список доменов верхнего уровня и количество потоков для использования.

![image](https://github.com/user-attachments/assets/3589eafa-76a8-4887-8772-3118b249a3a9)

![image](https://github.com/user-attachments/assets/a023353c-a86f-4d55-8a3c-55ef537743e4)

