import asyncio
import random
import string
import requests
from pystyle import Write, Colors, Box

# API URLs
DISCORD_API = 'https://discord.com/api/v9'
DISCORD_INVITE_URL = f'{DISCORD_API}/invites/'
DISCORD_TOKEN_VALIDATE_URL = f'{DISCORD_API}/users/@me'

# Async function to generate random Discord tokens
def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=59))  # Example token length

# Function to check if a token is valid
def check_token(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(DISCORD_TOKEN_VALIDATE_URL, headers=headers)
    return response.status_code == 200

# Async function to generate Nitro codes
def generate_nitro_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))  # Example Nitro code length

# Function to check Nitro code validity
def check_nitro_code(code):
    # Replace with actual Nitro code validation logic
    return False  # Example: always return False

# Function to generate and check proxies
def generate_proxy():
    return f'http://{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1024, 65535)}'

def check_proxy(proxy):
    try:
        response = requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
        return response.status_code == 200
    except:
        return False

# Function to display menu
async def show_menu():
    Write.Print(Box.DoubleLine("Discord Tool - Main Menu", width=50), Colors.green_to_cyan, interval=0.000)
    Write.Print("1. Generate User Tokens", Colors.green_to_cyan, interval=0.000)
    Write.Print("2. Generate Nitro Codes", Colors.green_to_cyan, interval=0.000)
    Write.Print("3. Generate Proxies", Colors.green_to_cyan, interval=0.000)
    Write.Print("4. Exit", Colors.green_to_cyan, interval=0.000)
    choice = Write.Input("Select an option: ", Colors.green_to_cyan, interval=0.000)
    return choice

# Function to handle user token generation and checking
async def generate_user_tokens():
    tokens = []
    valid_tokens = []
    while True:
        token = generate_token()
        tokens.append(token)
        valid = check_token(token)
        status = "Valid" if valid else "Invalid"
        Write.Print(f"Token: {token} - {status}", Colors.green_to_cyan if valid else Colors.red_to_yellow, interval=0.01)
        await asyncio.sleep(0.1)  # Adjust speed here

        if Write.Input("\nPress [ ENTER ] to stop generating, or any other key to continue...", Colors.green_to_cyan, interval=0.000):
            break

    Write.Print(f"\nValid Tokens ({len(valid_tokens)}):", Colors.green_to_cyan, interval=0.000)
    for token in valid_tokens:
        Write.Print(token, Colors.green_to_cyan, interval=0.000)

# Function to handle Nitro code generation and checking
async def generate_nitro_codes():
    codes = []
    valid_codes = []
    while True:
        code = generate_nitro_code()
        codes.append(code)
        valid = check_nitro_code(code)
        status = "Valid" if valid else "Invalid"
        Write.Print(f"Nitro Code: {code} - {status}", Colors.green_to_cyan if valid else Colors.red_to_yellow, interval=0.01)
        await asyncio.sleep(0.1)  # Adjust speed here

        if Write.Input("\nPress [ ENTER ] to stop generating, or any other key to continue...", Colors.green_to_cyan, interval=0.000):
            break

    Write.Print(f"\nValid Nitro Codes ({len(valid_codes)}):", Colors.green_to_cyan, interval=0.000)
    for code in valid_codes:
        Write.Print(code, Colors.green_to_cyan, interval=0.000)

# Function to handle proxy generation and checking
async def generate_proxies():
    proxies = []
    valid_proxies = []
    while True:
        proxy = generate_proxy()
        proxies.append(proxy)
        valid = check_proxy(proxy)
        status = "Valid" if valid else "Invalid"
        Write.Print(f"Proxy: {proxy} - {status}", Colors.green_to_cyan if valid else Colors.red_to_yellow, interval=0.01)
        await asyncio.sleep(0.1)  # Adjust speed here

        if Write.Input("\nPress [ ENTER ] to stop generating, or any other key to continue...", Colors.green_to_cyan, interval=0.000):
            break

    Write.Print(f"\nValid Proxies ({len(valid_proxies)}):", Colors.green_to_cyan, interval=0.000)
    for proxy in valid_proxies:
        Write.Print(proxy, Colors.green_to_cyan, interval=0.000)

# Main function
async def main():
    while True:
        choice = await show_menu()
        if choice == '1':
            await generate_user_tokens()
        elif choice == '2':
            await generate_nitro_codes()
        elif choice == '3':
            await generate_proxies()
        elif choice == '4':
            Write.Print("Exiting...", Colors.red_to_yellow, interval=0.000)
            break
        else:
            Write.Print("Invalid choice, please try again.", Colors.red_to_yellow, interval=0.000)

if __name__ == '__main__':
    asyncio.run(main())
