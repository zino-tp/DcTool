import asyncio
import requests
import random
import string
import threading
import sys
import select
from datetime import datetime

# Constants
DISCORD_API_URL = 'https://discord.com/api/v10'
VALIDATION_TIMEOUT = 10  # seconds

# Generate random Discord-like tokens
def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits + '._-', k=59))

def generate_nitro_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

def generate_proxy():
    return f"http://{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1024, 65535)}"

def generate_nitro_gift_link():
    return f"https://discord.gift/{generate_nitro_code()}"

# Validate tokens
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
def display_results(valid, invalid, label):
    if not valid and not invalid:
        print(f"\nNo {label} found")
        return
    print(f"\nValid {label}: {len(valid)}")
    for item in valid:
        print(f"  {item}")
    print(f"Invalid {label}: {len(invalid)}")
    for item in invalid:
        print(f"  {item}")

# Non-blocking input detection
def non_blocking_input(prompt):
    print(prompt, end='', flush=True)
    while True:
        if select.select([sys.stdin], [], [], 0.0)[0]:
            return sys.stdin.readline().strip()
        asyncio.run(asyncio.sleep(0.01))

# Asynchronous token generation and validation
async def generate_tokens():
    valid_tokens = []
    invalid_tokens = []

    print("Generating and validating tokens. Press [ENTER] to stop...")

    stop_event = threading.Event()

    def stop_generating():
        nonlocal stop_event
        input("Press [ENTER] to stop...")
        stop_event.set()

    threading.Thread(target=stop_generating).start()

    while not stop_event.is_set():
        token = generate_token()
        print(f"\033[92mGenerated Token:\033[0m {token}")
        if validate_token(token):
            valid_tokens.append(token)
            print(f"\033[92mValid Token:\033[0m {token}")
        else:
            invalid_tokens.append(token)
            print(f"\033[91mInvalid Token:\033[0m {token}")
        await asyncio.sleep(0.01)

    display_results(valid_tokens, invalid_tokens, "Tokens")

# Asynchronous Nitro code generation and validation
async def generate_nitro_codes():
    valid_nitro = []
    invalid_nitro = []

    print("Generating and validating Nitro codes. Press [ENTER] to stop...")

    stop_event = threading.Event()

    def stop_generating():
        nonlocal stop_event
        input("Press [ENTER] to stop...")
        stop_event.set()

    threading.Thread(target=stop_generating).start()

    while not stop_event.is_set():
        nitro_code = generate_nitro_code()
        nitro_link = generate_nitro_gift_link()
        print(f"\033[92mGenerated Nitro Link:\033[0m {nitro_link}")
        if validate_nitro_code(nitro_code):
            valid_nitro.append(nitro_link)
            print(f"\033[92mValid Nitro Link:\033[0m {nitro_link}")
        else:
            invalid_nitro.append(nitro_link)
            print(f"\033[91mInvalid Nitro Link:\033[0m {nitro_link}")
        await asyncio.sleep(0.01)

    display_results(valid_nitro, invalid_nitro, "Nitro Codes")

# Asynchronous Proxy generation and validation
async def generate_proxies():
    valid_proxies = []
    invalid_proxies = []

    print("Generating and validating proxies. Press [ENTER] to stop...")

    stop_event = threading.Event()

    def stop_generating():
        nonlocal stop_event
        input("Press [ENTER] to stop...")
        stop_event.set()

    threading.Thread(target=stop_generating).start()

    while not stop_event.is_set():
        proxy = generate_proxy()
        print(f"\033[92mGenerated Proxy:\033[0m {proxy}")
        if validate_proxy(proxy):
            valid_proxies.append(proxy)
            print(f"\033[92mValid Proxy:\033[0m {proxy}")
        else:
            invalid_proxies.append(proxy)
            print(f"\033[91mInvalid Proxy:\033[0m {proxy}")
        await asyncio.sleep(0.01)

    display_results(valid_proxies, invalid_proxies, "Proxies")

# Show menu with improved design
async def show_menu():
    print("\n\033[96m===============================\033[0m")
    print("\033[96m   Discord Tool - Main Menu   \033[0m")
    print("\033[96m===============================\033[0m")
    print("\033[93m1.\033[0m Token Generator & Checker")
    print("\033[93m2.\033[0m Nitro Code Generator & Checker")
    print("\033[93m3.\033[0m Proxy Generator & Checker")
    print("\033[93m4.\033[0m Exit")
    print("\033[96m===============================\033[0m")
    choice = input("\033[92mSelect an option: \033[0m")
    return choice

# Main function
async def main():
    while True:
        choice = await show_menu()
        if choice == '1':
            await generate_tokens()
        elif choice == '2':
            await generate_nitro_codes()
        elif choice == '3':
            await generate_proxies()
        elif choice == '4':
            print("\033[92mExiting...\033[0m")
            break
        else:
            print("\033[91mInvalid option. Please select again.\033[0m")
        input("\033[92mPress [ENTER] to continue...\033[0m")

if __name__ == '__main__':
    asyncio.run(main())
