import textwrap
import uuid
from moviepy.editor import *
from datetime import date

import random,os

TITLE_FONT_SIZE = 30
FONT_SIZE = 30
TITLE_FONT_COLOR = 'white'

BGM_PATH = 'assets/music/'
BGM_PATH += random.choice([x for x in os.listdir("assets/music") if os.path.isfile(os.path.join("assets/music", x))])

STATIC_PATH = 'assets/static.mp4'
BACKGROUND_PATH = 'assets/black.png'

ALIEN_PATH = 'assets/reddit aliens/'
ALIEN_PATH += random.choice([x for x in os.listdir("assets/reddit aliens") if os.path.isfile(os.path.join("assets/reddit aliens", x))])

SIZE = (1280, 720)
BG_COLOR = (16,16,16)
VIDEO_PATH = "data/video/"
FONT = 'Franklin-Gothic-Medium'


def generate_title(text, audio_path,page):
    #color_clip = ColorClip(SIZE, BG_COLOR)
    audio_clip = AudioFileClip(audio_path)
    audio_clip = audio_clip.fx(afx.volumex,0.7)
    font_size = TITLE_FONT_SIZE+20
    backGround_clip = ImageClip(page['background'])
    wrapped_text = textwrap.fill(text, width=50)
    txt_clip = TextClip(wrapped_text,fontsize=font_size, font=FONT, color=TITLE_FONT_COLOR, align="west")
    txt_clip = txt_clip.set_pos("center")
    clip = CompositeVideoClip([backGround_clip, txt_clip])
    clip.audio = audio_clip
    clip.duration = audio_clip.duration
    static_clip = VideoFileClip(STATIC_PATH)
    static_clip = static_clip.fx(afx.volumex, 0.15)
    clip = concatenate_videoclips([clip, static_clip])
    
    return clip

def generate_clip(post, comment,page):
    text = comment.body
    audio_path = comment.body_audio


    #color_clip = ColorClip(SIZE, BG_COLOR)
    backGround_clip = ImageClip(page['background'])
    alien_clip = ImageClip(ALIEN_PATH).set_position(('right','top'))
    logo_clip = ImageClip(page['logo']).set_position(('left','top')).resize(0.5)

    audio_clip = AudioFileClip(audio_path)
    audio_clip = audio_clip.fx(afx.volumex,0.7)
    font_size = TITLE_FONT_SIZE
    author_font_size = 20

    wrapped_text = textwrap.fill(text, width=70)
    txt_clip = TextClip(wrapped_text,fontsize=font_size, font=FONT, color=TITLE_FONT_COLOR, align="west", interline=2)
    txt_clip = txt_clip.set_pos("center")

    author_clip = TextClip(f"/u/{comment.author}", fontsize=author_font_size, font=FONT, color="lightblue")
    author_pos = (SIZE[0]/2 - txt_clip.size[0]/2, SIZE[1]/2 - txt_clip.size[1]/2 - author_font_size - 10)
    author_clip = author_clip.set_pos(author_pos)

    score_clip = TextClip(f"{comment.score} puntos", fontsize=author_font_size, font=FONT, color="grey")
    score_pos = (author_pos[0] + author_clip.size[0] + 20, author_pos[1])
    score_clip = score_clip.set_pos(score_pos)

    #clip = CompositeVideoClip([backGround_clip,alien_clip,logo_clip, txt_clip, author_clip, score_clip]) #With Alien and logo
    clip = CompositeVideoClip([backGround_clip, txt_clip, author_clip, score_clip]) #Without Alien and no logo

    clip.audio = audio_clip
    clip.duration = audio_clip.duration
    static_clip = VideoFileClip(STATIC_PATH)
    static_clip = static_clip.fx(afx.volumex, 0.15)
    clip = concatenate_videoclips([clip, static_clip])
    return clip

def generate_video_Text(context):
    post = context["post"]
    clips = []
    clips.append(generate_title(post.title, post.title_audio,context['page']))
    for comment in post.comments:
        if len(comment.body)<900:    
            comment_clip = generate_clip(post, comment,context['page'])
            # overlay reply
            if comment.reply:
                # TODO this
                pass
            clips.append(comment_clip)
    video = concatenate_videoclips(clips)
    background_audio_clip = AudioFileClip(BGM_PATH)
    background_audio_clip = afx.audio_loop(background_audio_clip, duration=video.duration)
    background_audio_clip = background_audio_clip.fx(afx.volumex, 0.1)
    video.audio = CompositeAudioClip([video.audio, background_audio_clip])
    video_id = uuid.uuid4()
    path = f"{VIDEO_PATH}{video_id}.mp4"
    context["video_path"] = path
    context["video_id"] = video_id
    video.write_videofile(path, fps=24, codec='libx264', threads=4)

def generate_video(context):
    if context['page']['video'] == True:
        return generate_video_Video(context)
    else:
        return generate_video_Text(context)

def generate_clip_video(video,page):
    
    backGround_clip = ImageClip(page['background'])
    print(video['video_path'])
    video_clip = VideoFileClip(video['video_path'])
    video_clip = video_clip.set_position(("center"))
    if video['height'] > 576 or video['height'] >500:
        video_clip = video_clip.resize(height=576)
    if video['height']<300:    
        video_clip = video_clip.resize(height=400)
    if video['width']>950:
        video_clip = video_clip.resize(width=950)

    video_clip = video_clip.fx(afx.volumex,0.35)

    text = video['title']

    font_size = 30
    author_font_size = 20

    wrapped_text = textwrap.fill(text, width=70)
    txt_clip = TextClip(wrapped_text,fontsize=font_size, font=FONT, color=TITLE_FONT_COLOR, align="center", interline=2)
    txt_clip = txt_clip.set_position((SIZE[0]/2-txt_clip.size[0]/2,10))

    author_clip = TextClip(f"by: /u/{video['author']}", fontsize=author_font_size, font=FONT, color=TITLE_FONT_COLOR)
    author_pos = (SIZE[0]/2 + txt_clip.size[0]/2, txt_clip.size[1])
    author_clip = author_clip.set_position(author_pos)

    logo_clip = ImageClip(page['logo'])
    logo_clip = logo_clip.resize((125,125))
    logo_clip = logo_clip.set_position((SIZE[0]-logo_clip.size[0]-50,60))
    #score_clip = TextClip(f"{comment.score} puntos", fontsize=author_font_size, font=FONT, color="grey")
    #score_pos = (author_pos[0] + author_clip.size[0] + 20, author_pos[1])
    #score_clip = score_clip.set_pos(score_pos)

    #clip = CompositeVideoClip([backGround_clip,alien_clip,logo_clip, txt_clip, author_clip, score_clip]) #With Alien and logo
    clip = CompositeVideoClip([backGround_clip, video_clip,txt_clip,author_clip,logo_clip]) #Without Alien and no logo

    #clip.audio = audio_clip
    clip.duration = video_clip.duration
    static_clip = VideoFileClip(STATIC_PATH)
    static_clip = static_clip.fx(afx.volumex, 0.15)
    clip = concatenate_videoclips([clip, static_clip])
    return clip

def generate_video_Video(context):
    post = context["post"]
    clips = []

    for video in post:
        comment_clip = generate_clip_video(video,context['page'])           
        clips.append(comment_clip)


    video = concatenate_videoclips(clips)
    background_audio_clip = AudioFileClip(BGM_PATH)
    background_audio_clip = afx.audio_loop(background_audio_clip, duration=video.duration)
    background_audio_clip = background_audio_clip.fx(afx.volumex, 0.1)
    video.audio = CompositeAudioClip([video.audio, background_audio_clip])
    video_id = uuid.uuid4()
    path = f"{VIDEO_PATH}{video_id}.mp4"
    context["video_path"] = path
    context["video_id"] = video_id
    video.write_videofile(path, fps=24, codec='libx264', threads=4)