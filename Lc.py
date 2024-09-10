import asyncio
import random
import string
import aiohttp
import os
from pystyle import Write, Colors, Box

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

async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    Write.Print("╔════════════════════════════════════════════════╗", Colors.green_to_cyan, interval=0.000)
    Write.Print("║          Discord Tool - Main Menu              ║", Colors.green_to_cyan, interval=0.000)
    Write.Print("╚════════════════════════════════════════════════╝", Colors.green_to_cyan, interval=0.000)

    while True:
        Write.Print("1. Generate and Check Tokens", Colors.yellow_to_red, interval=0.000)
        Write.Print("2. Generate and Check Proxies", Colors.yellow_to_red, interval=0.000)
        Write.Print("3. Generate and Check Nitro Codes", Colors.yellow_to_red, interval=0.000)
        Write.Print("4. Exit", Colors.yellow_to_red, interval=0.000)
        choice = input("Choose an option: ")

        if choice == '1':
            count = int(input("Enter the number of tokens to generate: "))
            Write.Print("Generating tokens... Please wait.", Colors.yellow_to_red, interval=0.000)
            async with aiohttp.ClientSession() as session:
                valid_tokens, invalid_tokens = await generate_and_check_tokens(session, count)
            Write.Print(f"Valid Tokens: {len(valid_tokens)}", Colors.green, interval=0.000)
            Write.Print(f"Invalid Tokens: {len(invalid_tokens)}", Colors.red, interval=0.000)
            if not valid_tokens:
                Write.Print("No valid tokens found.", Colors.red, interval=0.000)
            if not invalid_tokens:
                Write.Print("No invalid tokens found.", Colors.red, interval=0.000)
            Write.Print("1. Generate Again", Colors.yellow_to_red, interval=0.000)
            Write.Print("2. Show Valid Tokens", Colors.yellow_to_red, interval=0.000)
            Write.Print("3. Show Invalid Tokens", Colors.yellow_to_red, interval=0.000)
            Write.Print("4. Go Back", Colors.yellow_to_red, interval=0.000)
            sub_choice = input("Choose an option: ")
            if sub_choice == '1':
                continue
            elif sub_choice == '2':
                Write.Print("\nValid Tokens:\n" + "\n".join(valid_tokens), Colors.green, interval=0.000)
            elif sub_choice == '3':
                Write.Print("\nInvalid Tokens:\n" + "\n".join(invalid_tokens), Colors.red, interval=0.000)
            elif sub_choice == '4':
                continue

        elif choice == '2':
            count = int(input("Enter the number of proxies to generate: "))
            Write.Print("Generating proxies... Please wait.", Colors.yellow_to_red, interval=0.000)
            proxies = await generate_proxies(count)
            valid_proxies, invalid_proxies = await check_proxies(proxies)
            Write.Print(f"Valid Proxies: {len(valid_proxies)}", Colors.green, interval=0.000)
            Write.Print(f"Invalid Proxies: {len(invalid_proxies)}", Colors.red, interval=0.000)
            if not valid_proxies:
                Write.Print("No valid proxies found.", Colors.red, interval=0.000)
            if not invalid_proxies:
                Write.Print("No invalid proxies found.", Colors.red, interval=0.000)
            Write.Print("1. Generate Again", Colors.yellow_to_red, interval=0.000)
            Write.Print("2. Show Valid Proxies", Colors.yellow_to_red, interval=0.000)
            Write.Print("3. Show Invalid Proxies", Colors.yellow_to_red, interval=0.000)
            Write.Print("4. Go Back", Colors.yellow_to_red, interval=0.000)
            sub_choice = input("Choose an option: ")
            if sub_choice == '1':
                continue
            elif sub_choice == '2':
                Write.Print("\nValid Proxies:\n" + "\n".join(valid_proxies), Colors.green, interval=0.000)
            elif sub_choice == '3':
                Write.Print("\nInvalid Proxies:\n" + "\n".join(invalid_proxies), Colors.red, interval=0.000)
            elif sub_choice == '4':
                continue

        elif choice == '3':
            count = int(input("Enter the number of Nitro codes to generate: "))
            Write.Print("Generating Nitro codes... Please wait.", Colors.yellow_to_red, interval=0.000)
            async with aiohttp.ClientSession() as session:
                valid_codes, invalid_codes = await generate_and_check_nitro_codes(session, count)
            Write.Print(f"Valid Nitro Codes: {len(valid_codes)}", Colors.green, interval=0.000)
            Write.Print(f"Invalid Nitro Codes: {len(invalid_codes)}", Colors.red, interval=0.000)
            if not valid_codes:
                Write.Print("No valid Nitro codes found.", Colors.red, interval=0.000)
            if not invalid_codes:
                Write.Print("No invalid Nitro codes found.", Colors.red, interval=0.000)
            Write.Print("1. Generate Again", Colors.yellow_to_red, interval=0.000)
            Write.Print("2. Show Valid Nitro Codes", Colors.yellow_to_red, interval=0.000)
            Write.Print("3. Show Invalid Nitro Codes", Colors.yellow_to_red, interval=0.000)
            Write.Print("4. Go Back", Colors.yellow_to_red, interval=0.000)
            sub_choice = input("Choose an option: ")
            if sub_choice == '1':
                continue
            elif sub_choice == '2':
                Write.Print("\nValid Nitro Codes:\n" + "\n".join(valid_codes), Colors.green, interval=0.000)
            elif sub_choice == '3':
                Write.Print("\nInvalid Nitro Codes:\n" + "\n".join(invalid_codes), Colors.red, interval=0.000)
            elif sub_choice == '4':
                continue

        elif choice == '4':
            Write.Print("Exiting...", Colors.red_to_yellow, interval=0.000)
            break

        else:
            Write.Print("Invalid choice. Please try again.", Colors.red_to_yellow, interval=0.000)

if __name__ == '__main__':
    asyncio.run(main())
