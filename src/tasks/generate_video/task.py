import textwrap
import uuid
from moviepy.editor import *
from googletrans import Translator
import random,os

TITLE_FONT_SIZE = 30
FONT_SIZE = 40
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
    audio_clip = audio_clip.fx(afx.volumex,0.5)
    font_size = TITLE_FONT_SIZE
    backGround_clip = ImageClip(page['background'])
    wrapped_text = textwrap.fill(text, width=90)
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
    audio_clip = audio_clip.fx(afx.volumex,0.5)
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

    clip = CompositeVideoClip([backGround_clip,alien_clip,logo_clip, txt_clip, author_clip, score_clip])
    clip.audio = audio_clip
    clip.duration = audio_clip.duration
    static_clip = VideoFileClip(STATIC_PATH)
    static_clip = static_clip.fx(afx.volumex, 0.15)
    clip = concatenate_videoclips([clip, static_clip])
    return clip

def generate_video(context):
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
    background_audio_clip = background_audio_clip.fx(afx.volumex, 0.05)
    video.audio = CompositeAudioClip([video.audio, background_audio_clip])
    video_id = uuid.uuid4()
    path = f"{VIDEO_PATH}{video_id}.mp4"
    context["video_path"] = path
    context["video_id"] = video_id
    video.write_videofile(path, fps=24, codec='libx264', threads=4)

