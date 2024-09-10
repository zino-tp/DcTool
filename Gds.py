import asyncio
import requests
import random
import string

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
        print(f"No {label} found")
        return
    print(f"Valid {label}: {len(valid)}")
    for item in valid:
        print(f"  {item}")
    print(f"Invalid {label}: {len(invalid)}")
    for item in invalid:
        print(f"  {item}")

# Asynchronous token generation and validation
async def generate_tokens():
    valid_tokens = []
    invalid_tokens = []
    print("Generating and validating tokens. Press [ENTER] to stop...")
    while True:
        token = generate_token()
        print(f"Generated Token: {token}")
        if validate_token(token):
            valid_tokens.append(token)
            print(f"Valid Token: {token}")
        else:
            invalid_tokens.append(token)
            print(f"Invalid Token: {token}")
        await asyncio.sleep(0.2)
        if input() == "":
            break
    display_results(valid_tokens, invalid_tokens, "Tokens")

# Asynchronous Nitro code generation and validation
async def generate_nitro_codes():
    valid_nitro = []
    invalid_nitro = []
    print("Generating and validating Nitro codes. Press [ENTER] to stop...")
    while True:
        nitro_code = generate_nitro_code()
        print(f"Generated Nitro Code: {nitro_code}")
        if validate_nitro_code(nitro_code):
            valid_nitro.append(nitro_code)
            print(f"Valid Nitro Code: {nitro_code}")
        else:
            invalid_nitro.append(nitro_code)
            print(f"Invalid Nitro Code: {nitro_code}")
        await asyncio.sleep(0.2)
        if input() == "":
            break
    display_results(valid_nitro, invalid_nitro, "Nitro Codes")

# Asynchronous Proxy generation and validation
async def generate_proxies():
    valid_proxies = []
    invalid_proxies = []
    print("Generating and validating proxies. Press [ENTER] to stop...")
    while True:
        proxy = generate_proxy()
        print(f"Generated Proxy: {proxy}")
        if validate_proxy(proxy):
            valid_proxies.append(proxy)
            print(f"Valid Proxy: {proxy}")
        else:
            invalid_proxies.append(proxy)
            print(f"Invalid Proxy: {proxy}")
        await asyncio.sleep(0.2)
        if input() == "":
            break
    display_results(valid_proxies, invalid_proxies, "Proxies")

# Show menu
async def show_menu():
    print("\nDiscord Tool - Main Menu")
    print("1. Token Generator & Checker")
    print("2. Nitro Code Generator & Checker")
    print("3. Proxy Generator & Checker")
    print("4. Exit")
    choice = input("Select an option: ")
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
            print("Exiting...")
            break
        else:
            print("Invalid option. Please select again.")
        input("Press [ENTER] to continue...")

if __name__ == '__main__':
    asyncio.run(main())
