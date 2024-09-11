import asyncio
import random
import string
from aiohttp import ClientSession
import time
from termcolor import colored

# Farben für die Konsolenausgabe
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"

# Utility-Funktion zum Zeichnen der Box
def draw_box(title, content):
    border = '=' * (len(title) + 4)
    print(f"{border}\n{Colors.CYAN}{title.center(len(border))}{Colors.RESET}\n{border}")
    print(content)
    print(border)

# Token-Generator-Funktion
async def token_generator(session):
    while True:
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=59))
        valid = await token_checker(session, token)
        if valid:
            print(f"{Colors.GREEN}[VALID] {token}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[INVALID] {token}{Colors.RESET}")
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

# Menü-Anzeige und Benutzerinteraktion
async def show_menu():
    while True:
        draw_box("Discord Tool - Main Menu", "1. Generate Discord Tokens\n2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Generating Discord Tokens... Press Enter to stop.")
            async with ClientSession() as session:
                await generate_until_stopped(token_generator, session)
        elif choice == '2':
            break
        else:
            print(f"{Colors.RED}Invalid choice, please try again.{Colors.RESET}")

# Funktion zum kontinuierlichen Generieren bis zur Eingabe
async def generate_until_stopped(generator, *args):
    task = asyncio.create_task(generator(*args))
    while True:
        if input() == '':
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            break

# Hauptfunktion zum Starten des Programms
async def main():
    await show_menu()

if __name__ == "__main__":
    asyncio.run(main())
