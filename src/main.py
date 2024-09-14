from twitch import *
from database import *

def main():
    streamers = get_random_streamer(5)

    for streamer in streamers:
        ide = get_streamer_id(streamer)
        clips = get_clips_url(streamer_id=ide, start_date=get_start_date(), end_date=get_end_date())
        
        add_clips(clips=clips)

        clips_to_use = get_random_clip(number=4)
        
if __name__ == "__main__":
    main()