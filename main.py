import os
import base64
import random
import requests
import pyfiglet
import webbrowser
from pypresence import Presence
import time

DISCORD_WEBHOOK = 'aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTE4MzM3MjYzOTQ4MjQyOTUxMS9LS0ZfZDNrSXV5VnFSbG9XdkgwLXJLcVNaSVJSVWRaTzZUVy1qZjU3ZTczUnY3WWVNTmx1SnhNQ3A4Nk1SQlBLajdIZg=='
CLIENT_ID = '1057398643574964325'
LARGE_IMAGE_KEY = 'https://cdn.discordapp.com/attachments/1131043505075126393/1183390476963938374/Zenith.png?ex=65882944&is=6575b444&hm=1f8e932a20742bfefe342809e2c26618545b0a01453f93b41145ef78d609213f&'

def decrypt_webhook_url(encoded_url):
    return base64.b64decode(encoded_url).decode('utf-8')

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def generate_username(base_username, special_character):
    og_username = f'{base_username[:len(base_username)//2]}{special_character}{base_username[len(base_username)//2:]}'
    return og_username

def print_logo():
    logo_text = "Zenith"
    font = "doom"
    ascii_art = pyfiglet.figlet_format(logo_text, font=font)
    print("\033[94m" + ascii_art + "\033[0m")  # Blue color

def get_special_characters():
    url = 'https://pastebin.com/raw/3VjwF0Q0'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip().split('\n')
    else:
        print(f"Failed to fetch special characters. Using default.")
        return ['ﱞ']

def open_discord_server():
    discord_server_url = 'https://discord.gg/stWgVnBgHq'
    webbrowser.open(discord_server_url)

def clear_username_file():
    with open('username.txt', 'w', encoding='utf-8') as file:
        file.write('')  # Clears the content of the file

def send_to_discord_webhook(message, username):
    embed = {
        'title': 'Zenith | Username Generator',
        'description': message,
        'color': 3447003,  # Blue color
    }

    data = {'embeds': [embed]}
    requests.post(decrypt_webhook_url(DISCORD_WEBHOOK), json=data)

def update_discord_rich_presence(details, state):
    try:
        RPC.update(details=details, state=state, large_image=LARGE_IMAGE_KEY)
    except Exception as e:
        print(f"Error updating Discord Rich Presence: {e}")

if __name__ == "__main__":
    base_username = ""
    special_characters = get_special_characters()

    RPC = Presence(CLIENT_ID)
    RPC.connect()

    clear_username_file()

    while True:
        clear_screen()
        print_logo()
        print("\033[94m[1] Generate Username\033[0m")
        print("\033[94m[2] Support Server\033[0m")
        print("\033[94m[3] Exit\033[0m")

        choice = input("\033[94m\nEnter Option from 1-3: \033[0m")
        if choice == "1":
            if not base_username:
                base_username = input("Insert Desired Username: ")

            special_character = random.choice(special_characters)
            og_username = generate_username(base_username, special_character)
            print("Generated OG Fortnite username:", og_username)

            # Save to file
            with open('username.txt', 'a', encoding='utf-8') as file:
                file.write(og_username + '\n')

            # Send to Discord webhook with embed
            send_to_discord_webhook(f"Generated OG Fortnite username: ``{og_username}``", og_username)

            # Update Discord Rich Presence
            update_discord_rich_presence(details=f"Generated username: {og_username}", state=f"Last action: Generating username")

            input("Press Enter to continue...")

        elif choice == "2":
            open_discord_server()

        elif choice == "3":
            print("Exiting program. Goodbye!")
            # Close the Discord Rich Presence connection
            RPC.close()
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
            input("Press Enter to continue...")
