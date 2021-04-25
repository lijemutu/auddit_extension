from tasks.scrape_reddit.task import get_hottest_post
from tasks.scrape_reddit.tiktok import dwn_tiktok
from tasks.text_to_speech.task import tts
from tasks.generate_video.task import generate_video, generate_tiktok
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
                upload_video,
                cleanup
            ]
        if page['video'] == True:
             self.tasks = [
                get_hottest_post,
                generate_video,
                upload_video,
                cleanup
            ]
        if page['video'] =="tiktok":
            self.tasks = [
                dwn_tiktok,
                generate_tiktok,
                upload_video,
                cleanup
            ]

        self.context = dict()

    def execute(self, **kwargs):
        self.context = kwargs
        for task in self.tasks:
            print(f"Current Task: {task.__name__}")          
            task(self.context)    # do stuff



if __name__ == "__main__":
    paginas =['next_level_videos','redditVideos', 'Otra_pagina_que_sube_recopilaciones_de_TikTok',\
    'Pagina_que_hace_compilaciones_perronas_de_tiktok.json','preguntasRedditColombia','preguntas_reddit_mex']
    #paginas =['Pagina_que_hace_compilaciones_perronas_de_tiktok']

    for pagina in paginas:
        with open('doc/'+pagina+'.json',encoding='utf-8') as page:
            page = json.load(page)
            pipeline = Pipeline(page)
            pipeline.execute(nsfw=False, comment_limit=20,page=page)
