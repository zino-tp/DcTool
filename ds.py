import asyncio
import random
import string
import aiohttp
import os
from pystyle import Write, Colors

# Helper Functions
def generate_random_token(length=24):
    return ''.join(random.choices(string.ascii_letters + string.digits + '.-', k=length))

async def check_token(session, token):
    headers = {'Authorization': token}
    async with session.get('https://discord.com/api/v10/users/@me', headers=headers) as response:
        if response.status == 200:
            return token
        else:
            return None

async def generate_and_check_tokens(session, count):
    valid_tokens = []
    invalid_tokens = []
    for _ in range(count):
        token = generate_random_token()
        result = await check_token(session, token)
        if result:
            valid_tokens.append(result)
        else:
            invalid_tokens.append(token)
        Write.Print(f"Generated Token: {token}", Colors.cyan, interval=0.000)
    return valid_tokens, invalid_tokens

async def proxy_checker(proxy):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://httpbin.org/ip', proxy=f"http://{proxy}", timeout=5) as response:
                if response.status == 200:
                    return proxy
                else:
                    return None
    except:
        return None

async def generate_proxies(count):
    proxies = [f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1000, 9999)}" for _ in range(count)]
    return proxies

async def check_proxies(proxies):
    tasks = [proxy_checker(proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)
    valid_proxies = [proxy for proxy in results if proxy]
    invalid_proxies = [proxy for proxy in proxies if proxy not in valid_proxies]
    return valid_proxies, invalid_proxies

async def generate_nitro_codes(count):
    return [''.join(random.choices(string.ascii_letters + string.digits, k=16)) for _ in range(count)]

async def check_nitro_code(session, code):
    async with session.get(f'https://discord.com/api/v10/entitlements/gift-codes/{code}') as response:
        if response.status == 200:
            return f"https://discord.com/gifts/{code}"
        else:
            return None

async def generate_and_check_nitro_codes(session, count):
    valid_codes = []
    invalid_codes = []
    codes = await generate_nitro_codes(count)
    for code in codes:
        result = await check_nitro_code(session, code)
        if result:
            valid_codes.append(result)
        else:
            invalid_codes.append(code)
        Write.Print(f"Generated Nitro Code: {code}", Colors.cyan, interval=0.000)
    return valid_codes, invalid_codes

def print_box(title, content):
    os.system('cls' if os.name == 'nt' else 'clear')
    width = 50
    print(f"+{'-' * (width - 2)}+")
    print(f"| {title.center(width - 2)} |")
    print(f"+{'-' * (width - 2)}+")
    for line in content:
        print(f"| {line.ljust(width - 2)} |")
    print(f"+{'-' * (width - 2)}+")

async def display_results(valid_items, invalid_items, valid_label, invalid_label):
    os.system('cls' if os.name == 'nt' else 'clear')
    print_box(valid_label, valid_items if valid_items else ["No valid items found."])
    print_box(invalid_label, invalid_items if invalid_items else ["No invalid items found."])

async def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_box("Discord Tool - Main Menu", [
        "1. Generate and Check Tokens",
        "2. Generate and Check Proxies",
        "3. Generate and Check Nitro Codes",
        "4. Exit"
    ])

    while True:
        choice = input("\nChoose an option: ")

        if choice == '1':
            count = int(input("Enter the number of tokens to generate: "))
            Write.Print("Generating tokens... Please wait.", Colors.yellow_to_red, interval=0.000)
            async with aiohttp.ClientSession() as session:
                valid_tokens, invalid_tokens = await generate_and_check_tokens(session, count)
            await display_results(valid_tokens, invalid_tokens, "Valid Tokens", "Invalid Tokens")
            while True:
                Write.Print("\n1. Generate Again", Colors.yellow_to_red, interval=0.000)
                Write.Print("2. Show Valid Tokens", Colors.yellow_to_red, interval=0.000)
                Write.Print("3. Show Invalid Tokens", Colors.yellow_to_red, interval=0.000)
                Write.Print("4. Go Back", Colors.yellow_to_red, interval=0.000)
                sub_choice = input("\nChoose an option: ")
                if sub_choice == '1':
                    break
                elif sub_choice == '2':
                    await display_results(valid_tokens, [], "Valid Tokens", "No Invalid Tokens")
                elif sub_choice == '3':
                    await display_results([], invalid_tokens, "No Valid Tokens", "Invalid Tokens")
                elif sub_choice == '4':
                    break

        elif choice == '2':
            count = int(input("Enter the number of proxies to generate: "))
            Write.Print("Generating proxies... Please wait.", Colors.yellow_to_red, interval=0.000)
            proxies = await generate_proxies(count)
            valid_proxies, invalid_proxies = await check_proxies(proxies)
            await display_results(valid_proxies, invalid_proxies, "Valid Proxies", "Invalid Proxies")
            while True:
                Write.Print("\n1. Generate Again", Colors.yellow_to_red, interval=0.000)
                Write.Print("2. Show Valid Proxies", Colors.yellow_to_red, interval=0.000)
                Write.Print("3. Show Invalid Proxies", Colors.yellow_to_red, interval=0.000)
                Write.Print("4. Go Back", Colors.yellow_to_red, interval=0.000)
                sub_choice = input("\nChoose an option: ")
                if sub_choice == '1':
                    break
                elif sub_choice == '2':
                    await display_results(valid_proxies, [], "Valid Proxies", "No Invalid Proxies")
                elif sub_choice == '3':
                    await display_results([], invalid_proxies, "No Valid Proxies", "Invalid Proxies")
                elif sub_choice == '4':
                    break

        elif choice == '3':
            count = int(input("Enter the number of Nitro codes to generate: "))
            Write.Print("Generating Nitro codes... Please wait.", Colors.yellow_to_red, interval=0.000)
            async with aiohttp.ClientSession() as session:
                valid_codes, invalid_codes = await generate_and_check_nitro_codes(session, count)
            await display_results(valid_codes, invalid_codes, "Valid Nitro Codes", "Invalid Nitro Codes")
            while True:
                Write.Print("\n1. Generate Again", Colors.yellow_to_red, interval=0.000)
                Write.Print("2. Show Valid Nitro Codes", Colors.yellow_to_red, interval=0.000)
                Write.Print("3. Show Invalid Nitro Codes", Colors.yellow_to_red, interval=0.000)
                Write.Print("4. Go Back", Colors.yellow_to_red, interval=0.000)
                sub_choice = input("\nChoose an option: ")
                if sub_choice == '1':
                    break
                elif sub_choice == '2':
                    await display_results(valid_codes, [], "Valid Nitro Codes", "No Invalid Nitro Codes")
                elif sub_choice == '3':
                    await display_results([], invalid_codes, "No Valid Nitro Codes", "Invalid Nitro Codes")
                elif sub_choice == '4':
                    break

        elif choice == '4':
            Write.Print("Returning to Main Menu...", Colors.red_to_yellow, interval=0.000)
            await asyncio.sleep(1)
            continue

        else:
            Write.Print("Invalid choice. Please try again.", Colors.red_to_yellow, interval=0.000)

if __name__ == '__main__':
    asyncio.run(menu())
