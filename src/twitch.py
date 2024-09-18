import requests
import os
import urllib

from database import *
from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    
def get_start_date():
    seven_days_ago = datetime.today() - timedelta(days=7)
    formatted_date = seven_days_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

    return formatted_date

def get_end_date():
    formatted_date = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")

    return formatted_date

def get_access_token():
    url = f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials"
    
    res = requests.post(url=url)
    
    return res.json()["access_token"]
    
access_token = get_access_token()

def get_clips_url(start_date: str, end_date: str, streamer_id: str = "", game_id: str = ""):
    url = f"https://api.twitch.tv/helix/clips?broadcaster_id={streamer_id}&started_at={start_date}&ended_at={end_date}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Client-Id": CLIENT_ID
    }
    
    res = requests.get(url=url, headers=headers)
    
    data = res.json()["data"]

    clips = []

    for clip in data:
        clips.append({"url": clip["url"],"title":clip["title"],"streamer":clip["broadcaster_name"]})
        
    return clips

def get_streamer_id(channel_name: str):
    url = f"https://api.twitch.tv/helix/users?login={channel_name}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Client-Id": CLIENT_ID
    }
    
    res = requests.get(url=url, headers=headers)
    
    return res.json()["data"][0]["id"]

def download_clip(clip_url: str, clip_name: str, path: str):
    ### https://production.assets.clips.twitchcdn.net/v2/media/<id>/video.mp4?sig=<sig>&token=<token>
    
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0",
    }
    
    clip_id = clip_url.split("/")[-1]
    
    url = f"https://cy49zmt23f.execute-api.us-east-1.amazonaws.com/dev/download_clip?id={clip_id}"
    
    res = requests.get(url=url, headers=headers).json()
    
    video_url = res["data"][0]["video_url"]
    
    clip_name += ".mp4"

    urllib.request.urlretrieve(video_url, path+clip_name) 