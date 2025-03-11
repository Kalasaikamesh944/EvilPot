#!/usr/bin/env python3

import socket
import threading
import logging
import time
import os
import sys
from scapy.all import sniff, IP
from collections import defaultdict

# Configure logging
logging.basicConfig(filename='evilpot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

attack_logs = []

# ANSI Escape Codes
CYAN = '\033[1;36m'
MAGENTA = '\033[1;35m'
GREEN = '\033[1;32m'
RED = '\033[1;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
ORANGE = '\033[38;5;208m'
PURPLE = '\033[1;35m'
RESET = '\033[0m'

# Cyberpunk Banner
BANNER = f"""
{RED}▓█████▄  ██▀███   ██▓ ██▒   █▓ ▄▄▄       ███▄ ▄███▓
▓█   ▀▄█▒▓██ ▒ ██▒▓██▒▓██░   █▒▒████▄    ▓██▒▀█▀ ██▒
▒███  █▄▒▓██ ░▄█ ▒▒██▒ ▓██  █▒░▒██  ▀█▄  ▓██    ▓██░
▒▓█▄   █▒▒██▀▀█▄  ░██░  ▒██ █░░░██▄▄▄▄██ ▒██    ▒██ 
▒ ▓█████▄░██▓ ▒██▒░██░   ▒▀█░   ▓█   ▓██▒▒██▒   ░██▒
░ ░▒ ▒  ░░ ▒▓ ░▒▓░░▓     ░ ▐░   ▒▒   ▓▒█░░ ▒░   ░  ░
  ░  ▒   ░▒ ░ ▒░ ▒ ░   ░ ░░    ▒   ▒▒ ░░  ░      ░
░         ░   ░  ▒ ░     ░░    ░   ▒   ░      ░   
░ ░       ░     ░        ░        ░  ░       ░    
░                 ░                                
{MAGENTA}───────────────────────────────────────────────
{BLUE}    EVILPOT HONEYPOT v2.0 - By KTMC
{MAGENTA}───────────────────────────────────────────────{RESET}
"""

def slowprint(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# Function to display logs in xterm with cyberpunk styling
def display_logs():
    while True:
        os.system('clear')
        print(BANNER)
        print(f"{CYAN}╔══════════════════════════════════════════╗")
        print(f"║{YELLOW}    LIVE ATTACK MONITOR - LAST 10 EVENTS    {CYAN}║")
        print(f"╚══════════════════════════════════════════╝{RESET}")
        
        for log in attack_logs[-10:]:
            if "SSH" in log:
                print(f"{GREEN}▐▶{RESET} {log}")
            elif "HTTP" in log:
                print(f"{BLUE}▐▶{RESET} {log}")
            elif "HTTPS" in log:
                print(f"{PURPLE}▐▶{RESET} {log}")
            elif "FTP" in log:
                print(f"{ORANGE}▐▶{RESET} {log}")
            else:
                print(f"{RED}▐▶{RESET} {log}")
        
        print(f"\n{CYAN}╔══════════════════════════════════════════╗")
        print(f"║{MAGENTA}    ACTIVE THREATS    {YELLOW}LOGS: {len(attack_logs)}    {CYAN}║")
        print(f"╚══════════════════════════════════════════╝{RESET}\n")
        time.sleep(1)

# Realistic Fake SSH Service
def fake_ssh_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 22))
    server.listen(5)
    slowprint(f"{GREEN}[+] SSH Honeypot Running on 0.0.0.0:22...{RESET}", 0.02)
    
    while True:
        client, addr = server.accept()
        ip = addr[0]
        log_entry = f"{GREEN}SSH Connection Attempt: {ip}{RESET}"
        logging.info(log_entry)
        attack_logs.append(log_entry)
        
        # Send SSH banner
        client.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3\r\n")
        
        # Simulate username prompt
        client.send(b"Username: ")
        username = client.recv(1024).decode().strip()
        
        # Simulate password prompt
        client.send(b"Password: ")
        password = client.recv(1024).decode().strip()
        
        # Log credentials
        password_entry = f"{GREEN}SSH Login Attempt - Username: {username}, Password: {password}, IP: {ip}{RESET}"
        logging.info(password_entry)
        attack_logs.append(password_entry)
        
        # Simulate authentication failure
        client.send(b"Permission denied (publickey,password).\r\n")
        client.close()

# Realistic Fake HTTP Service
def fake_http_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 80))
    server.listen(5)
    slowprint(f"{BLUE}[+] HTTP Honeypot Running on 0.0.0.0:80...{RESET}", 0.02)
    
    while True:
        client, addr = server.accept()
        ip = addr[0]
        log_entry = f"{BLUE}HTTP Connection Attempt: {ip}{RESET}"
        logging.info(log_entry)
        attack_logs.append(log_entry)
        
        # Simulate HTTP response
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<html><body><h1>Welcome to Admin Panel</h1></body></html>"
        )
        client.send(response.encode())
        client.close()

# Realistic Fake HTTPS Service
def fake_https_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 443))
    server.listen(5)
    slowprint(f"{PURPLE}[+] HTTPS Honeypot Running on 0.0.0.0:443...{RESET}", 0.02)
    
    while True:
        client, addr = server.accept()
        ip = addr[0]
        log_entry = f"{PURPLE}HTTPS Connection Attempt: {ip}{RESET}"
        logging.info(log_entry)
        attack_logs.append(log_entry)
        
        # Simulate HTTPS response
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<html><body><h1>Secure Admin Panel</h1></body></html>"
        )
        client.send(response.encode())
        client.close()

# Realistic Fake FTP Service
def fake_ftp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 21))
    server.listen(5)
    slowprint(f"{ORANGE}[+] FTP Honeypot Running on 0.0.0.0:21...{RESET}", 0.02)
    
    while True:
        client, addr = server.accept()
        ip = addr[0]
        log_entry = f"{ORANGE}FTP Connection Attempt: {ip}{RESET}"
        logging.info(log_entry)
        attack_logs.append(log_entry)
        
        # Send FTP banner
        client.send(b"220 Welcome to Fake FTP Server\r\n")
        
        # Handle FTP commands
        while True:
            data = client.recv(1024).decode().strip()
            if not data:
                break
            
            if data.startswith("USER"):
                username = data.split(" ")[1]
                client.send(b"331 Please specify the password.\r\n")
            elif data.startswith("PASS"):
                password = data.split(" ")[1]
                log_entry = f"{ORANGE}FTP Login Attempt - Username: {username}, Password: {password}, IP: {ip}{RESET}"
                logging.info(log_entry)
                attack_logs.append(log_entry)
                client.send(b"530 Login incorrect.\r\n")
            else:
                client.send(b"500 Unknown command.\r\n")
        
        client.close()

if __name__ == "__main__":
    os.system('xterm-256color')
    os.system('clear')
    slowprint(BANNER, 0.01)
    slowprint(f"{GREEN}[+] Initializing DarkNet Protocols...{RESET}", 0.05)
    slowprint(f"{BLUE}[+] Activating KTMC  Defense Matrix...{RESET}", 0.05)
    
    threading.Thread(target=fake_ssh_server, daemon=True).start()
    threading.Thread(target=fake_http_server, daemon=True).start()
    threading.Thread(target=fake_https_server, daemon=True).start()
    threading.Thread(target=fake_ftp_server, daemon=True).start()
    threading.Thread(target=display_logs, daemon=True).start()
    
    slowprint(f"\n{YELLOW}[!] EvilPot Honeypot Active on:{RESET}", 0.05)
    slowprint(f"{CYAN}    SSH: 0.0.0.0:22  |  HTTP: 0.0.0.0:80  |  HTTPS: 0.0.0.0:443  |  FTP: 0.0.0.0:21{RESET}", 0.02)
    slowprint(f"{MAGENTA}[*] Press CTRL+C to exit...{RESET}\n", 0.05)
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        slowprint(f"\n{RED}[!] Terminating Honeypot...{RESET}", 0.05)
        slowprint(f"{GREEN}[+] System secured. Returning to reality...{RESET}\n", 0.05)
        sys.exit(0)
