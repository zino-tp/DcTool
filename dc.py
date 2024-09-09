import aiohttp
import asyncio
import os
import random
import string
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel

console = Console()

# Function to generate a random user token
def generate_token(length=24):
    return ''.join(random.choices(string.ascii_letters + string.digits + '._', k=length))

# Function to generate a random Nitro code
def generate_nitro_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Function to check if the token is valid and try to join a server
async def check_token_and_join(session, token, server_id):
    url = f"https://discord.com/api/v9/guilds/{server_id}/members/@me"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
    }

    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                join_url = f"https://discord.com/api/v9/guilds/{server_id}/members/@me"
                async with session.put(join_url, headers=headers) as join_response:
                    if join_response.status == 201:
                        return f"Success: {token}", "green"
                    else:
                        return f"Failed to join: {token}", "red"
            elif response.status == 401:
                return f"Invalid Token: {token}", "red"
            else:
                return f"Unknown Status ({response.status}): {token}", "yellow"
    except Exception as e:
        return f"Error: {e}", "red"

# Function to generate and check Nitro codes
async def generate_and_check_nitro(session, webhook_url, count):
    nitro_codes = [generate_nitro_code() for _ in range(count)]
    valid_codes = []
    
    for code in nitro_codes:
        url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}"
        async with session.get(url) as response:
            if response.status == 200:
                valid_codes.append(code)
                # Send valid code to webhook
                webhook_data = {'content': f"Valid Nitro Code: https://discord.com/gifts/{code}"}
                async with session.post(webhook_url, json=webhook_data) as webhook_response:
                    if webhook_response.status == 204:
                        console.print(f"Valid Nitro Code Sent: https://discord.com/gifts/{code}", style="green")
                    else:
                        console.print(f"Failed to Send Valid Nitro Code: {webhook_response.status}", style="red")
            else:
                console.print(f"Invalid Nitro Code: https://discord.com/gifts/{code}", style="red")

# Main function to handle user input and menu
async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel("[bold cyan]Discord Token Checker & Nitro Generator[/bold cyan]", title="Welcome", border_style="cyan"))

    menu_choice = Prompt.ask("[bold]Choose an option:[/bold]\n1. Generate and Check Nitro Codes\n2. Generate and Check User Tokens\n3. Exit", choices=["1", "2", "3"])
    
    if menu_choice == "1":
        webhook_url = Prompt.ask("Enter the Discord Webhook URL", default="your_webhook_url")
        count = Prompt.ask("How many Nitro codes do you want to generate and check?", default="10")
        try:
            count = int(count)
        except ValueError:
            console.print("[red]Invalid number. Exiting...[/red]")
            return
        
        async with aiohttp.ClientSession() as session:
            await generate_and_check_nitro(session, webhook_url, count)
    
    elif menu_choice == "2":
        server_id = Prompt.ask("Enter the server ID you want to join", default="your_server_id")
        num_tokens = Prompt.ask("How many tokens do you want to generate?", default="10")
        try:
            num_tokens = int(num_tokens)
        except ValueError:
            console.print("[red]Invalid number of tokens. Exiting...[/red]")
            return
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(num_tokens):
                token = generate_token()
                tasks.append(check_token_and_join(session, token, server_id))
            
            results = await asyncio.gather(*tasks)
        
        for result, color in results:
            console.print(Text(result, style=color))
        
        console.print("[bold green]Finished processing all tokens![/bold green]")
    
    elif menu_choice == "3":
        console.print("[bold cyan]Exiting...[/bold cyan]")

if __name__ == '__main__':
    asyncio.run(main())
