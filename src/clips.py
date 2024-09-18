import ffmpeg
import os

def get_videos_paths(directory: str):
    file_paths = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    return file_paths

def create_video(filename:str, videos_directory: list = []):
    videos_paths = get_videos_paths(directory=videos_directory)
    
    ffmpeg.concat([video for video in videos_paths]).output(filename)