from tasks.scrape_reddit.task import get_hottest_post
from tasks.text_to_speech.task import tts
from tasks.generate_video.task import generate_video
from tasks.upload_video.task import upload_video
from tasks.generate_thumbnail.task import generate_thumbnail
from tasks.cleanup.task import cleanup
import prawcore,gtts,json

class Pipeline:
    def __init__(self,page):
        if page['video'] == False:
            self.tasks = [
                get_hottest_post,
                tts,
                generate_video,
                generate_thumbnail,
                #upload_video
                cleanup
            ]
        else:
             self.tasks = [
                get_hottest_post,
                generate_video,
                #upload_video
                cleanup
            ]
        self.context = dict()

    def execute(self, **kwargs):
        self.context = kwargs
        for task in self.tasks:
            print(f"Current Task: {task.__name__}")          
            task(self.context)    # do stuff



if __name__ == "__main__":
    #paginas =['next_level_videos','redditVideos','preguntas_reddit_mex','preguntasRedditColombia']
    paginas =['redditVideos']

    for pagina in paginas:
        with open('doc/'+pagina+'.json') as page:
            page = json.load(page)
            pipeline = Pipeline(page)
            pipeline.execute(nsfw=False, comment_limit=20,page=page)
