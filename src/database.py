import pymongo
import pymongo.database

import requests

from bs4 import BeautifulSoup

CLIENT = pymongo.MongoClient(host="localhost:27017")

DB_NAME = "twitch_clips"
DATABASE = pymongo.database.Database(client=CLIENT, name=DB_NAME)

clips_collection = DATABASE.get_collection(name="clips")
musics = DATABASE.get_collection(name="musics")
streamers_collection = DATABASE.get_collection(name="streamers")

def add_clips(clips: list = []):
    for clip in clips:
        if not clips_collection.find_one({"url": clip["url"]}):
            clips_collection.insert_one({"url": clip["url"], "title": clip["title"], "streamer": clip["streamer"]})

def add_streamer(streamer: str):
    streamers_collection.insert_one({"name": streamer})

def reset_streamers():
    streamers_collection.delete_many()

def get_random_streamer(number: int):
    s = []
    
    for _ in range(number):
        streamers = streamers_collection.aggregate([{"$sample": {"size": 3}}])
        
        for streamer in streamers:
            name = streamer.get("name")
            
            if name not in s:
                s.append(name)
            
    return s

def get_random_music():
    return musics.find_one()

def remove_clip(clip):
    clips_collection.delete_one({"url": clip["url"]})

def get_random_clip(number: int):
    clips = []
    
    for _ in range(number):
        clip = clips_collection.find_one()
        
        if clip not in clips:
            clips.append(clip)
            
            remove_clip(clip=clip)
            
    return clips

def get_trending_streamers():
    streamers = []
    
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0"
    }
    
    url = "https://twitchtracker.com/channels/ranking/french"
    
    res = requests.get(url=url, headers=headers)
    
    soup = BeautifulSoup(res.text, "html.parser")
    
    with open("index.html", "w") as f:
        f.write(res.text)
            
    all_tr = soup.find("tbody").find_all("tr")
    
    for tr in all_tr:        
        lines = tr.find_all("td")
        
        for td in lines:
            if "#" not in td.text:    
                name = td.find("a")

                if name != None :
                    name = name.attrs["href"].replace("/", "")
                    if name not in streamers:
                        streamers.append(name)
        
    return streamers
        
def every_month():
    streamers = get_trending_streamers()
    for streamer in streamers:
        add_streamer(streamer=streamer)