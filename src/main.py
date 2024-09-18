from twitch import *
from database import *
from clips import *

def main():
    streamers = get_random_streamer(5)
    
    path = "C:\\Users\\Salmen\\Desktop\\Python Projects\\AutomaticTiktokClips\\src\\videos\\"

    for i, streamer in enumerate(streamers):        
        ide = get_streamer_id(streamer)
        clips = get_clips_url(streamer_id=ide, start_date=get_start_date(), end_date=get_end_date())
        
        add_clips(clips=clips)

        clips_to_use = get_random_clips(1)
        
        for clip in clips_to_use:
            print(f"Clip {i+1}")
            
            download_clip(clip_url=clip.get("url"), clip_name=f"clip{i}", path=path)
        
    create_video(filename="output.mp4", videos_directory=path)    
    
if __name__ == "__main__":
    main()