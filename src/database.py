import pymongo
import pymongo.database

CLIENT = pymongo.MongoClient(host="localhost:27017")

DB_NAME = "twitch_clips"
DATABASE = pymongo.database.Database(client=CLIENT, name=DB_NAME)

clips = DATABASE.get_collection(name="clips")
musics = DATABASE.get_collection(name="musics")
used_clips = DATABASE.get_collection(name="used_clips")
streamers = DATABASE.get_collection(name="streamers")

def add_clip():
    pass

def add_streamer():
    pass

def add_used_clip():
    pass

def add_clip():
    pass