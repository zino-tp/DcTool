import asyncio
import aiohttp
import random
import string
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from time import sleep

console = Console()

# Design Panels
def banner():
    console.print(Panel.fit("Welcome to the Ultimate Discord Tool", style="bold green"))

def menu():
    console.print(Panel.fit("""
[1] Generate User Tokens + Server Joiner
[2] Generate Nitro Codes + Checker
[3] Generate Proxies + Checker
    """, style="bold blue"))

# Helper functions
def generate_user_token():
    # Generate a realistic Discord user token
    part1 = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    part2 = ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=6))
    part3 = ''.join(random.choices(string.ascii_letters + string.digits, k=27))
    return f"{part1}.{part2}.{part3}"

def generate_nitro_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def generate_proxy():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1000, 9999)}"

async def check_token(token, server_id):
    url = f"https://discord.com/api/v9/invites/{server_id}"
    headers = {'Authorization': token}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    console.print(f"[bold green]Valid Token: {token} - Joined Server!")
                else:
                    console.print(f"[bold red]Invalid Token: {token}")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}")

async def check_nitro(nitro_code):
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{nitro_code}?with_application=false&with_subscription_plan=true"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    console.print(f"[bold green]Valid Nitro Code: https://discord.com/gifts/{nitro_code}")
                else:
                    console.print(f"[bold red]Invalid Nitro Code: https://discord.com/gifts/{nitro_code}")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}")

async def check_proxy(proxy):
    url = "http://example.com"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=f"http://{proxy}") as response:
                if response.status == 200:
                    console.print(f"[bold green]Valid Proxy: {proxy}")
                    return True
                else:
                    console.print(f"[bold red]Invalid Proxy: {proxy}")
                    return False
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}")
        return False

# Main functions
async def generate_user_tokens_and_joiner():
    server_id = Prompt.ask("[bold cyan]Enter Server ID")
    token_amount = int(Prompt.ask("[bold cyan]How many User Tokens do you want to generate?"))
    
    valid_tokens = 0
    invalid_tokens = 0
    console.print("[bold yellow]Generating User Tokens and trying to join server...[/bold yellow]")
    for _ in range(token_amount):
        token = generate_user_token()
        console.print(f"[bold blue]Generated User Token: {token}")
        await check_token(token, server_id)
        sleep(0.3)

    console.print(f"[bold green]Summary: {valid_tokens} valid tokens, {invalid_tokens} invalid tokens")

async def generate_nitro_codes_and_check():
    nitro_amount = int(Prompt.ask("[bold cyan]How many Nitro Codes do you want to generate?"))
    webhook_url = Prompt.ask("[bold cyan]Enter Webhook URL (for valid codes)")
    
    valid_nitros = 0
    invalid_nitros = 0

    console.print("[bold yellow]Generating Nitro Codes...[/bold yellow]")
    for _ in range(nitro_amount):
        nitro_code = generate_nitro_code()
        console.print(f"[bold blue]Generated Nitro Code: https://discord.com/gifts/{nitro_code}")
        await check_nitro(nitro_code)
        sleep(0.1)
    
    console.print(f"[bold green]Summary: {valid_nitros} valid Nitro codes, {invalid_nitros} invalid Nitro codes")

async def generate_proxies_and_check():
    proxy_amount = int(Prompt.ask("[bold cyan]How many Proxies do you want to generate?"))
    
    valid_proxies = 0
    invalid_proxies = 0
    console.print("[bold yellow]Generating Proxies and checking validity...[/bold yellow]")
    for _ in range(proxy_amount):
        proxy = generate_proxy()
        console.print(f"[bold blue]Generated Proxy: {proxy}")
        valid = await check_proxy(proxy)
        if valid:
            valid_proxies += 1
        else:
            invalid_proxies += 1
        sleep(0.3)

    console.print(f"[bold green]Summary: {valid_proxies} valid proxies, {invalid_proxies} invalid proxies")

# Main execution
async def main():
    banner()
    menu()
    
    choice = int(Prompt.ask("[bold cyan]Choose an option"))
    
    if choice == 1:
        await generate_user_tokens_and_joiner()
    elif choice == 2:
        await generate_nitro_codes_and_check()
    elif choice == 3:
        await generate_proxies_and_check()
    else:
        console.print("[bold red]Invalid option![/bold red]")

if __name__ == "__main__":
    asyncio.run(main())
