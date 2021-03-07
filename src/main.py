from tasks.scrape_reddit.task import get_hottest_post
from tasks.text_to_speech.task import tts
from tasks.generate_video.task import generate_video
from tasks.upload_video.task import upload_video
from tasks.generate_thumbnail.task import generate_thumbnail
from tasks.cleanup.task import cleanup
import prawcore,gtts

class Pipeline:
    def __init__(self):
        self.tasks = [
            #get_hottest_post,
            #tts,
            #generate_video,
            #generate_thumbnail
            #upload_video
            cleanup
        ]
        self.context = dict()

    def execute(self, **kwargs):
        self.context = kwargs
        for task in self.tasks:
            print(f"Current Task: {task.__name__}")          
            while True:
                try:
                    task(self.context)    # do stuff
                
                except gtts.tts.gTTSError:
                    print(f"Retrying: {task.__name__}")
                    continue
                break


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.execute(subreddit='askreddit', nsfw=False, comment_limit=10)
