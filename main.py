import requests
from dotenv import load_dotenv
from pathlib import Path
import os
import webbrowser

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)
twitch_web = "https://www.twitch.tv/"

def get_app_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "client_credentials"
    }
    r = requests.post(url, params=params)
    r.raise_for_status()
    return r.json()["access_token"]

def is_streamer_live(username, token):
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": os.getenv("CLIENT_ID"),
        "Authorization": f"Bearer {token}"
    }
    params = {"user_login": username}

    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()

    data = r.json()["data"]
    # print("API Response Data:", data)  # Debugging line to check the response data
    return len(data) > 0

def get_streamer_input():
    streamer = input("Enter the Twitch streamer username: ").strip()
    return streamer

if __name__ == "__main__":
    token = get_app_token()
    streamer = get_streamer_input()

    if is_streamer_live(streamer, token):
        print(f"{streamer} is LIVE 🔴")
        webbrowser.open(twitch_web + streamer)
    else:
        print(f"{streamer} is offline")
        
