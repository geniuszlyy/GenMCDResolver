import os
import socket
import sys
import re
from os import system, environ, getenv
from platform import platform
from colorama import init, Fore, Style
import ctypes
from time import time, sleep
import threading
import requests
import ipaddress

# Инициализация colorama
init(autoreset=True)

class MinecraftResolver:
    # Диапазоны IP-адресов Cloudflare
    CLOUDFLARE_IP_RANGES = [
        "103.21.244.0/22",
        "103.22.200.0/22",
        "103.31.4.0/22",
        "104.16.0.0/13",
        "104.24.0.0/14",
        "108.162.192.0/18",
        "131.0.72.0/22",
        "141.101.64.0/18",
        "162.158.0.0/15",
        "172.64.0.0/13",
        "173.245.48.0/20",
        "188.114.96.0/20",
        "190.93.240.0/20",
        "197.234.240.0/22",
        "198.41.128.0/17",
    ]

    def __init__(self):
        self.discovered_ips = set()  # Сет для хранения уникальных IP-адресов
        self.total_attempts = 0  # Общее количество попыток разрешения
        self.results = []  # Список для хранения результатов 
        self.checked_domains = 0  # Количество проверенных доменов
        self.total_domains = 0  # Общее количество доменов для проверки

    def display_logo(self):
        # логотип программы
        print(f"""
{Fore.LIGHTYELLOW_EX}   _____            __  __  _____ _____  _____                 _                
  / ____|          |  \/  |/ ____|  __ \|  __ \               | |               
 | |  __  ___ _ __ | \  / | |    | |  | | |__) |___  ___  ___ | |_   _____ _ __ 
 | | |_ |/ _ \ '_ \| |\/| | |    | |  | |  _  // _ \/ __|/ _ \| \ \ / / _ \ '__|
 | |__| |  __/ | | | |  | | |____| |__| | | \ \  __/\__ \ (_) | |\ V /  __/ |   
  \_____|\___|_| |_|_|  |_|\_____|_____/|_|  \_\___||___/\___/|_| \_/ \___|_|   
                                                                                
{Fore.LIGHTRED_EX}                     · Modern Minecraft Domain Resolver ·
                            · by geniuszly ·
        """)

# функция обработки параметров командной строки
    def parse_parameters(self):
        if len(sys.argv) > 1:
            if sys.argv[1] == "--unique":
                environ['unique_only'] = "true"
            elif sys.argv[1] == "-h":
                print(f"""
{Fore.LIGHTYELLOW_EX}   _____            __  __  _____ _____  _____                 _                
  / ____|          |  \/  |/ ____|  __ \|  __ \               | |               
 | |  __  ___ _ __ | \  / | |    | |  | | |__) |___  ___  ___ | |_   _____ _ __ 
 | | |_ |/ _ \ '_ \| |\/| | |    | |  | |  _  // _ \/ __|/ _ \| \ \ / / _ \ '__|
 | |__| |  __/ | | | |  | | |____| |__| | | \ \  __/\__ \ (_) | |\ V /  __/ |   
  \_____|\___|_| |_|_|  |_|\_____|_____/|_|  \_\___||___/\___/|_| \_/ \___|_|   
                                                                                
{Fore.LIGHTRED_EX}                     · Modern Minecraft Domain Resolver ·
                            · by geniuszly ·
        """)
                print(f"""
    {Fore.LIGHTYELLOW_EX}╭───────────────────────━━━━━━━━━━━━━━━━━━━━━───────────────────╮
    | {Fore.LIGHTBLUE_EX}Использование » {Fore.LIGHTGREEN_EX}python {os.path.basename(__file__)}                                {Fore.LIGHTYELLOW_EX}| 
    | {Fore.LIGHTCYAN_EX} -> показывает как уникальные, так и уже найденные IP-адреса  {Fore.LIGHTYELLOW_EX}|
    | {Fore.LIGHTBLUE_EX}Использование » {Fore.LIGHTGREEN_EX}python {os.path.basename(__file__)} --unique                       {Fore.LIGHTYELLOW_EX}|
    | {Fore.LIGHTCYAN_EX} -> показывает только уникальные IP-адреса                    {Fore.LIGHTYELLOW_EX}|
    ╰───────────────────────━━━━━━━━━━━━━━━━━━━━━───────────────────╯
    """)
                sys.exit()

# функция установки заголовка терминала
    def set_console_title(self, title):
        if "windows" in platform().lower():
            ctypes.windll.kernel32.SetConsoleTitleA(title.encode())
        else:
            sys.stdout.write(f"\x1b]2;{title}\x07")

 # функция очистки экрана терминала
    def clear_console(self):
        if "windows" in platform().lower():
            system("cls")
        else:
            system("clear")

 # функция проверки домена на допустимые символы
    def validate_domain(self, domain):
        return bool(re.match(r'^[a-zA-Z0-9.-]+$', domain))

# функция для разрешения домена и вывод результата
    def check_and_print_domain(self, full_domain):
        ip_address = self.resolve_domain(full_domain)
        if not ip_address:
            return False

        is_cloudflare = self.is_cloudflare_ip(ip_address)
        cloudflare_label = f"{Fore.LIGHTBLUE_EX} (Cloudflare)" if is_cloudflare else ""
        line_color = Fore.GREEN if not is_cloudflare else Fore.YELLOW
        
        if ip_address not in self.discovered_ips:
            self.discovered_ips.add(ip_address)
            result = f"{full_domain} -> {ip_address}{cloudflare_label}"
            self.results.append(result)
            print(f"{line_color}{result}{Style.RESET_ALL}")

        return True

# функция резольва домена в IP-адрес
    def resolve_domain(self, domain):
        self.set_console_title(f"(время выполнения {str(int(time()) - int(getenv('start_time')))} секунд) Minecraft Resolver - проверка '{domain}'")
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            return None

# функция загрузки списка слов из файла
    def load_wordlist(self, path):
        with open(path, "r") as file:
            return file.read().splitlines()

# функция для обработки поддоменов
    def process_subdomain(self, subdomain, top_level_domains, domain):
        for tld in top_level_domains:
            full_domain = f"{subdomain}.{domain}.{tld}"
            self.check_and_print_domain(full_domain)

# функция основной логики программы
    def main(self):
        self.clear_console()
        self.parse_parameters()
        self.display_logo()
        self.set_console_title("GenMCDResolver by geniuszly")

        domain = input(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Введите домен: ")
        if not self.validate_domain(domain):
            print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» {Fore.LIGHTYELLOW_EX} Неверный домен. Пожалуйста, введите правильное доменное имя (например, example.com).")
            sys.exit()

        environ['start_time'] = str(int(time()))

        subdomain_list_file = input(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Введите список поддоменов (по умолчанию: subdomains.txt): ") or "subdomains.txt"
        top_level_domain_list_file = input(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Введите список доменов верхнего уровня (по умолчанию: toplevels.txt): ") or "toplevels.txt"

        subdomains = self.load_wordlist(subdomain_list_file)
        top_level_domains = self.load_wordlist(top_level_domain_list_file)
        self.total_domains = len(subdomains) * len(top_level_domains)

        try:
            num_threads = int(input(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Введите количество потоков (по умолчанию: 20): ") or 20)
        except ValueError:
            num_threads = 20

        lines_per_thread = max(1, len(subdomains) // num_threads)

        # Создание и запуск потоков для обработки поддоменов
        threads = []
        for i in range(0, len(subdomains), lines_per_thread):
            subdomain_chunk = subdomains[i:i + lines_per_thread]
            thread = threading.Thread(target=self.process_subdomain_chunk, args=(subdomain_chunk, top_level_domains, domain))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        total_time = int(time()) - int(getenv('start_time'))
        print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Операция заняла {Fore.LIGHTGREEN_EX}{total_time} {Fore.LIGHTBLUE_EX}секунд")
        print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Найдено уникальных IP: {Fore.LIGHTGREEN_EX}{len(self.discovered_ips)}")
        print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Всего попыток: {Fore.LIGHTGREEN_EX}{self.total_attempts}")

        save_results = input(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Хотите сохранить результаты в файл? (да/нет): ").lower()
        if save_results == 'да':
            self.save_results() 

# функция обработки пачки поддоменов в отдельном потоке
    def process_subdomain_chunk(self, subdomains, top_level_domains, domain):
        for subdomain in subdomains:
            self.process_subdomain(subdomain, top_level_domains, domain)

# функция сохранения результатов в файл
    def save_results(self):
        filename = input(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Введите имя файла для сохранения (по умолчанию: results.txt): ") or "results.txt"
        with open(filename, 'w') as file:
           for result in self.results:
                file.write(f"{result}\n")
        print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenMCDResolver {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Результаты сохранены в {Fore.LIGHTGREEN_EX}{filename}")

# функция проверяет, принадлежит ли IP-адрес диапазону Cloudflare
    def is_cloudflare_ip(self, ip):
        ip_addr = ipaddress.ip_address(ip)
        for cidr in self.CLOUDFLARE_IP_RANGES:
            if ip_addr in ipaddress.ip_network(cidr):
                return True
        return False


if __name__ == "__main__":
    try:
        MinecraftResolver().main()
    except KeyboardInterrupt:
        sys.exit()
