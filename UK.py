import asyncio
import random
import string
import requests
import sys

# API URLs
DISCORD_API = 'https://discord.com/api/v9'
DISCORD_TOKEN_VALIDATE_URL = f'{DISCORD_API}/users/@me'

# Generate a random Discord token
def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=59))  # Example token length

# Check if a token is valid
def check_token(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(DISCORD_TOKEN_VALIDATE_URL, headers=headers)
    return response.status_code == 200

# Generate a random Nitro code
def generate_nitro_code():
    return f'https://discord.gift/{''.join(random.choices(string.ascii_letters + string.digits, k=16))}'

# Check Nitro code validity (Mock function, replace with actual API if available)
def check_nitro_code(code):
    # Replace with actual Nitro code validation logic
    return False  # Example: always return False

# Generate a random proxy
def generate_proxy():
    return f'http://{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1024, 65535)}'

# Check if a proxy is valid
def check_proxy(proxy):
    try:
        response = requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
        return response.status_code == 200
    except:
        return False

# Display menu
def display_menu():
    print("\n===================================")
    print("Discord Tool - Main Menu")
    print("===================================")
    print("1. Generate User Tokens")
    print("2. Generate Nitro Codes")
    print("3. Generate Proxies")
    print("4. Exit")
    print("===================================")
    choice = input("Select an option: ")
    return choice

# Function to generate user tokens
async def generate_user_tokens():
    tokens = []
    valid_tokens = []
    while True:
        token = generate_token()
        tokens.append(token)
        valid = check_token(token)
        status = "Valid" if valid else "Invalid"
        print(f"\nToken: {token} - {status}")
        if valid:
            valid_tokens.append(token)
        await asyncio.sleep(0.01)  # Adjust speed here
        if input("\nPress [ ENTER ] to stop generating, or any other key to continue...") == "":
            break
    return valid_tokens, tokens

# Function to generate Nitro codes
async def generate_nitro_codes():
    codes = []
    valid_codes = []
    while True:
        code = generate_nitro_code()
        codes.append(code)
        valid = check_nitro_code(code)
        status = "Valid" if valid else "Invalid"
        print(f"\nNitro Code: {code} - {status}")
        if valid:
            valid_codes.append(code)
        await asyncio.sleep(0.01)  # Adjust speed here
        if input("\nPress [ ENTER ] to stop generating, or any other key to continue...") == "":
            break
    return valid_codes, codes

# Function to generate proxies
async def generate_proxies():
    proxies = []
    valid_proxies = []
    while True:
        proxy = generate_proxy()
        proxies.append(proxy)
        valid = check_proxy(proxy)
        status = "Valid" if valid else "Invalid"
        print(f"\nProxy: {proxy} - {status}")
        if valid:
            valid_proxies.append(proxy)
        await asyncio.sleep(0.01)  # Adjust speed here
        if input("\nPress [ ENTER ] to stop generating, or any other key to continue...") == "":
            break
    return valid_proxies, proxies

# Main function
async def main():
    while True:
        choice = display_menu()
        if choice == '1':
            valid_tokens, all_tokens = await generate_user_tokens()
            print("\nResults:")
            print(f"Valid Tokens ({len(valid_tokens)}):")
            for token in valid_tokens:
                print(token)
            print(f"\nAll Tokens ({len(all_tokens)}):")
            for token in all_tokens:
                print(token)
            await post_process()
        elif choice == '2':
            valid_codes, all_codes = await generate_nitro_codes()
            print("\nResults:")
            print(f"Valid Nitro Codes ({len(valid_codes)}):")
            for code in valid_codes:
                print(code)
            print(f"\nAll Nitro Codes ({len(all_codes)}):")
            for code in all_codes:
                print(code)
            await post_process()
        elif choice == '3':
            valid_proxies, all_proxies = await generate_proxies()
            print("\nResults:")
            print(f"Valid Proxies ({len(valid_proxies)}):")
            for proxy in valid_proxies:
                print(proxy)
            print(f"\nAll Proxies ({len(all_proxies)}):")
            for proxy in all_proxies:
                print(proxy)
            await post_process()
        elif choice == '4':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice, please try again.")

# Function to handle post-processing and menu navigation
async def post_process():
    while True:
        print("\nOptions after stopping:")
        print("1. Show Valid Results")
        print("2. Show Invalid Results")
        print("3. Go to Home Menu")
        print("4. Exit")
        option = input("Select an option: ")
        if option == '1':
            # Implement showing valid results
            pass
        elif option == '2':
            # Implement showing invalid results
            pass
        elif option == '3':
            return
        elif option == '4':
            sys.exit()
        else:
            print("Invalid option, please try again.")

if __name__ == '__main__':
    asyncio.run(main())
