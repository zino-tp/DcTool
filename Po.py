import random
import string
import asyncio
from aiohttp import ClientSession

# Farben für die Konsolenausgabe
class Colors:
    green = "\033[92m"
    red = "\033[91m"
    reset = "\033[0m"

# Utility-Funktion zum zentrierten Drucken
def print_centered(text):
    print(f"{text}".center(80))

# Utility-Funktion zum Zeichnen der Box
def draw_box(title, content):
    box = f"""
    {'='*50}
    {title.center(50)}
    {'-'*50}
    {content}
    {'='*50}
    """
    print(box)

# Token-Generator-Funktion
async def token_generator(session):
    while True:
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=59))
        valid = await token_checker(session, token)
        if valid:
            print(f"{Colors.green}[VALID] {token}{Colors.reset}")
        else:
            print(f"{Colors.red}[INVALID] {token}{Colors.reset}")
        await asyncio.sleep(0.01)

# Überprüfung der Token-Gültigkeit
async def token_checker(session, token):
    url = 'https://discord.com/api/v9/users/@me'
    headers = {'Authorization': f'Bearer {token}'}
    try:
        async with session.get(url, headers=headers) as response:
            return response.status == 200
    except Exception:
        return False

# Nitro-Generator-Funktion
async def nitro_generator(session):
    while True:
        nitro = 'https://discord.gift/' + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        valid = await nitro_checker(session, nitro)
        if valid:
            print(f"{Colors.green}[VALID] {nitro}{Colors.reset}")
        else:
            print(f"{Colors.red}[INVALID] {nitro}{Colors.reset}")
        await asyncio.sleep(0.01)

# Überprüfung der Nitro-Codes
async def nitro_checker(session, nitro):
    try:
        async with session.head(nitro) as response:
            return response.status == 302
    except Exception:
        return False

# Proxy-Generator-Funktion
async def proxy_generator():
    while True:
        proxy = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}:{random.randint(1000, 9999)}"
        valid = await proxy_checker(proxy)
        if valid:
            print(f"{Colors.green}[VALID] {proxy}{Colors.reset}")
        else:
            print(f"{Colors.red}[INVALID] {proxy}{Colors.reset}")
        await asyncio.sleep(0.01)

# Überprüfung der Proxys
async def proxy_checker(proxy):
    # Beispielhafte Überprüfung, hier müsste eine echte Prüfung erfolgen
    try:
        async with ClientSession() as session:
            async with session.get(f"http://{proxy}", timeout=5) as response:
                return response.status == 200
    except Exception:
        return False

# Menü-Anzeige und Benutzerinteraktion
async def show_menu():
    while True:
        print_centered("Discord Tool - Main Menu")
        print("1. Generate Discord Tokens")
        print("2. Generate Nitro Codes")
        print("3. Generate Proxies")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Generating Discord Tokens... Press Enter to stop.")
            async with ClientSession() as session:
                await generate_until_stopped(token_generator, session)
        elif choice == '2':
            print("Generating Nitro Codes... Press Enter to stop.")
            async with ClientSession() as session:
                await generate_until_stopped(nitro_generator, session)
        elif choice == '3':
            print("Generating Proxies... Press Enter to stop.")
            await generate_until_stopped(proxy_generator)
        elif choice == '4':
            break

# Funktion zum kontinuierlichen Generieren bis zur Eingabe
async def generate_until_stopped(generator, *args):
    task = asyncio.create_task(generator(*args))
    input()  # Warte darauf, dass der Benutzer Enter drückt
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

# Hauptfunktion zum Starten des Programms
async def main():
    await show_menu()

if __name__ == "__main__":
    asyncio.run(main())
