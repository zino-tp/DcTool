import asyncio
import requests
import random
import string
from pystyle import Write, Colors, Box
import time

# Constants
DISCORD_API_URL = 'https://discord.com/api/v10'
VALIDATION_TIMEOUT = 10  # seconds

# Generate random tokens, nitro codes, and proxies
def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits + '._-', k=59))

def generate_nitro_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

def generate_proxy():
    return f"http://{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1024, 65535)}"

# Validate tokens, nitro codes, and proxies
def validate_token(token):
    url = f'{DISCORD_API_URL}/users/@me'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        response = requests.get(url, headers=headers, timeout=VALIDATION_TIMEOUT)
        return response.status_code == 200
    except requests.RequestException:
        return False

def validate_nitro_code(code):
    url = f'{DISCORD_API_URL}/nitro/validate'
    data = {
        'code': code
    }
    try:
        response = requests.post(url, json=data, timeout=VALIDATION_TIMEOUT)
        return response.status_code == 200
    except requests.RequestException:
        return False

def validate_proxy(proxy):
    try:
        response = requests.get('http://example.com', proxies={'http': proxy, 'https': proxy}, timeout=VALIDATION_TIMEOUT)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Display results
def display_results(valid_tokens, invalid_tokens, valid_nitro, invalid_nitro, valid_proxies, invalid_proxies):
    Write.Print(Box.DoubleCube("Results", padding=(1, 1), color=Colors.green_to_cyan), interval=0.000)
    Write.Print(f"Valid Tokens: {len(valid_tokens)}", Colors.green_to_cyan, interval=0.000)
    for token in valid_tokens:
        Write.Print(f"  {token}", Colors.green_to_cyan, interval=0.000)
    Write.Print(f"Invalid Tokens: {len(invalid_tokens)}", Colors.red_to_yellow, interval=0.000)
    for token in invalid_tokens:
        Write.Print(f"  {token}", Colors.red_to_yellow, interval=0.000)
    Write.Print(f"Valid Nitro Codes: {len(valid_nitro)}", Colors.green_to_cyan, interval=0.000)
    for nitro in valid_nitro:
        Write.Print(f"  {nitro}", Colors.green_to_cyan, interval=0.000)
    Write.Print(f"Invalid Nitro Codes: {len(invalid_nitro)}", Colors.red_to_yellow, interval=0.000)
    for nitro in invalid_nitro:
        Write.Print(f"  {nitro}", Colors.red_to_yellow, interval=0.000)
    Write.Print(f"Valid Proxies: {len(valid_proxies)}", Colors.green_to_cyan, interval=0.000)
    for proxy in valid_proxies:
        Write.Print(f"  {proxy}", Colors.green_to_cyan, interval=0.000)
    Write.Print(f"Invalid Proxies: {len(invalid_proxies)}", Colors.red_to_yellow, interval=0.000)
    for proxy in invalid_proxies:
        Write.Print(f"  {proxy}", Colors.red_to_yellow, interval=0.000)
    Write.Print(Box.DoubleCube("", padding=(1, 1), color=Colors.green_to_cyan), interval=0.000)

async def generate_and_check():
    valid_tokens = []
    invalid_tokens = []
    valid_nitro = []
    invalid_nitro = []
    valid_proxies = []
    invalid_proxies = []

    # Token generation and validation
    Write.Print("Generating and validating tokens...", Colors.green_to_cyan, interval=0.000)
    for _ in range(10):  # Adjust range for more tokens
        token = generate_token()
        Write.Print(f"Generated Token: {token}", Colors.green_to_cyan, interval=0.000)
        if validate_token(token):
            valid_tokens.append(token)
        else:
            invalid_tokens.append(token)
        await asyncio.sleep(0.3)

    # Nitro code generation and validation
    Write.Print("Generating and validating Nitro codes...", Colors.green_to_cyan, interval=0.000)
    for _ in range(10):  # Adjust range for more codes
        nitro_code = generate_nitro_code()
        Write.Print(f"Generated Nitro Code: {nitro_code}", Colors.green_to_cyan, interval=0.000)
        if validate_nitro_code(nitro_code):
            valid_nitro.append(nitro_code)
        else:
            invalid_nitro.append(nitro_code)
        await asyncio.sleep(0.1)

    # Proxy generation and validation
    Write.Print("Generating and validating proxies...", Colors.green_to_cyan, interval=0.000)
    for _ in range(10):  # Adjust range for more proxies
        proxy = generate_proxy()
        Write.Print(f"Generated Proxy: {proxy}", Colors.green_to_cyan, interval=0.000)
        if validate_proxy(proxy):
            valid_proxies.append(proxy)
        else:
            invalid_proxies.append(proxy)
        await asyncio.sleep(0.3)

    # Display results
    display_results(valid_tokens, invalid_tokens, valid_nitro, invalid_nitro, valid_proxies, invalid_proxies)

async def show_menu():
    Write.Print(Box.DoubleCube("Discord Tool - Main Menu", padding=(1, 1), color=Colors.green_to_cyan), interval=0.000)
    Write.Print("1. Token Generator & Checker", Colors.green_to_cyan, interval=0.000)
    Write.Print("2. Nitro Code Generator & Checker", Colors.green_to_cyan, interval=0.000)
    Write.Print("3. Proxy Generator & Checker", Colors.green_to_cyan, interval=0.000)
    Write.Print("4. Exit", Colors.green_to_cyan, interval=0.000)
    choice = input("Select an option: ")
    return choice

async def main():
    while True:
        choice = await show_menu()
        if choice == '1':
            Write.Print("Starting Token Generator & Checker...", Colors.green_to_cyan, interval=0.000)
            await generate_and_check()
        elif choice == '2':
            Write.Print("Starting Nitro Code Generator & Checker...", Colors.green_to_cyan, interval=0.000)
            await generate_and_check()
        elif choice == '3':
            Write.Print("Starting Proxy Generator & Checker...", Colors.green_to_cyan, interval=0.000)
            await generate_and_check()
        elif choice == '4':
            Write.Print("Exiting...", Colors.green_to_cyan, interval=0.000)
            break
        else:
            Write.Print("Invalid option. Please select again.", Colors.red_to_yellow, interval=0.000)
        Write.Input("Press [ENTER] to continue...", Colors.purple_to_blue, interval=0.030)

if __name__ == '__main__':
    asyncio.run(main())
