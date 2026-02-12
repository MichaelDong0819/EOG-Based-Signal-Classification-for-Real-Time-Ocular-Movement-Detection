import os
import pandas as pd

def list_videos(directory_path):
    videos = []
    if not os.path.exists(directory_path):
        print(f"Error: The directory '{directory_path}' does not exist.")
        return []
    if not os.path.isdir(directory_path):
        print(f"Error: The path '{directory_path}' is not a directory.")
        return []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.mp4'):
                videos.append(os.path.join(root, file))
                
    return videos

def get_hazard_times(video_path):
    meta_path = video_path.replace('.mp4', '.txt')

    if not os.path.exists(meta_path):
        print(f"Error: The meta file '{meta_path}' does not exist.")
        return None
    
    df = pd.read_csv(meta_path, sep=',', header=None)
    return float(df[0][1]) - 1, float(df[1][1]) + 3