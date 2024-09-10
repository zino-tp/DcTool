import os
import time
import random
import string
import asyncio
from pystyle import Write, Colors, Box

# Helper Functions for Token Generation and Validation
def generate_user_token():
    """Generates a fake Discord-like user token."""
    part1 = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    part2 = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    part3 = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=27))
    return f"{part1}.{part2}.{part3}"

def validate_token(token):
    """Simulates validation of a Discord token."""
    # Reducing the chances of a valid token
    return random.choices([True, False], weights=[1, 9], k=1)[0]

def generate_nitro_code():
    """Generates a fake Nitro code."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def validate_nitro_code(nitro):
    """Simulates validation of a Nitro code."""
    # Reducing the chances of a valid nitro code
    return random.choices([True, False], weights=[1, 9], k=1)[0]

def generate_proxy():
    """Generates a random proxy address."""
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1000, 9999)}"

def validate_proxy(proxy):
    """Simulates validation of a proxy."""
    # Reducing the chances of a valid proxy
    return random.choices([True, False], weights=[1, 9], k=1)[0]

# Menu functions
async def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Box.DoubleCube("Discord Tool - Main Menu"))
    print("\n1. Generate User Tokens\n2. Generate and Validate Nitro Codes\n3. Generate and Validate Proxies\n4. Exit\n")
    choice = Write.Input("Select an option: ", Colors.green_to_blue, interval=0.05)
    return choice

async def token_gen_checker():
    valid_tokens = []
    invalid_tokens = []
    stop_generation = False

    print(Box.DoubleCube("User Token Generator and Checker"))
    print("\nGenerating tokens, press ENTER to stop...")

    async def wait_for_enter():
        nonlocal stop_generation
        input()
        stop_generation = True

    # Start the input waiting function
    asyncio.create_task(wait_for_enter())

    while not stop_generation:
        for _ in range(2):  # Generate two tokens per iteration
            token = generate_user_token()
            is_valid = validate_token(token)
            if is_valid:
                valid_tokens.append(token)
            else:
                invalid_tokens.append(token)
            print(f"Generated Token: {token} {'[Valid]' if is_valid else '[Invalid]'}")
        await asyncio.sleep(0.3)  # Speed control, 0.3 seconds delay

    print(f"\nGeneration stopped. {len(valid_tokens)} valid tokens, {len(invalid_tokens)} invalid tokens.")
    await show_results(valid_tokens, invalid_tokens)

async def nitro_gen_checker():
    valid_nitros = []
    invalid_nitros = []
    stop_generation = False

    print(Box.DoubleCube("Nitro Code Generator and Checker"))
    print("\nGenerating Nitro codes, press ENTER to stop...")

    async def wait_for_enter():
        nonlocal stop_generation
        input()
        stop_generation = True

    # Start the input waiting function
    asyncio.create_task(wait_for_enter())

    while not stop_generation:
        for _ in range(2):  # Generate two nitros per iteration
            nitro = generate_nitro_code()
            is_valid = validate_nitro_code(nitro)
            if is_valid:
                valid_nitros.append(nitro)
            else:
                invalid_nitros.append(nitro)
            print(f"Generated Nitro Code: {nitro} {'[Valid]' if is_valid else '[Invalid]'}")
        await asyncio.sleep(0.1)  # Speed control, 0.1 seconds delay

    print(f"\nGeneration stopped. {len(valid_nitros)} valid Nitro codes, {len(invalid_nitros)} invalid Nitro codes.")
    await show_results(valid_nitros, invalid_nitros)

async def proxy_gen_checker():
    valid_proxies = []
    invalid_proxies = []
    stop_generation = False

    print(Box.DoubleCube("Proxy Generator and Checker"))
    print("\nGenerating proxies, press ENTER to stop...")

    async def wait_for_enter():
        nonlocal stop_generation
        input()
        stop_generation = True

    # Start the input waiting function
    asyncio.create_task(wait_for_enter())

    while not stop_generation:
        for _ in range(2):  # Generate two proxies per iteration
            proxy = generate_proxy()
            is_valid = validate_proxy(proxy)
            if is_valid:
                valid_proxies.append(proxy)
            else:
                invalid_proxies.append(proxy)
            print(f"Generated Proxy: {proxy} {'[Valid]' if is_valid else '[Invalid]'}")
        await asyncio.sleep(0.2)  # Speed control, 0.2 seconds delay

    print(f"\nGeneration stopped. {len(valid_proxies)} valid proxies, {len(invalid_proxies)} invalid proxies.")
    await show_results(valid_proxies, invalid_proxies)

async def show_results(valid_list, invalid_list):
    print("\n1. Show Valid Results\n2. Show Invalid Results\n3. Go Back to Menu")
    choice = Write.Input("Select an option: ", Colors.green_to_blue, interval=0.05)
    
    if choice == '1':
        if valid_list:
            print("\nValid Results:")
            for item in valid_list:
                print(item)
        else:
            print("\nNo valid items found.")
    elif choice == '2':
        if invalid_list:
            print("\nInvalid Results:")
            for item in invalid_list:
                print(item)
        else:
            print("\nNo invalid items found.")
    
    await asyncio.sleep(2)  # Give some delay before returning to the main menu

# Main async function
async def main():
    while True:
        choice = await show_menu()
        
        if choice == '1':
            await token_gen_checker()
        elif choice == '2':
            await nitro_gen_checker()
        elif choice == '3':
            await proxy_gen_checker()
        elif choice == '4':
            print("Exiting the tool. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
