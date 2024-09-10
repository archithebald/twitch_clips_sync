import requests
import os

from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

def get_clips(streamer_id: str, game_id: str):
    url = "https://api.twitch.tv/helix/clips"