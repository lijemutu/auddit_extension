import os
import glob

paths = [
    #"./data/thumbnails/*.png",
    #"./data/video/*.mp4",
    "./data/audio/*.mp3",
    ".data/video/tmp_video/*.mp4"
    "*.mp4"
]

def cleanup(context):
    for path in paths:
        files = glob.glob(path)
        for f in files:
            os.remove(f)
