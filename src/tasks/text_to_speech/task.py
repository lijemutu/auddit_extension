import uuid
import time
import requests
import random
from gtts import gTTS
from googletrans import Translator


VOICES = ["Matthew", "Joey", "Kendra"] # English voices
VOICES = ["Mia"] # Spanish voice
AUDIO_PATH = "data/audio/"
TTSMP3_URL = "https://ttsmp3.com/makemp3_new.php"

def save_tts(text):
   try:
      form_data = {
            "msg": text,
            "lang": random.choice(VOICES),
            "source": "ttsmp3"
      }
      json = requests.post(TTSMP3_URL, form_data).json()
      url = json["URL"]
      filename = json["MP3"]
      mp3_file = requests.get(url)
      path = f"{AUDIO_PATH}{filename}"
      with open(path, "wb") as out_file:
         out_file.write(mp3_file.content)
      return path
   except:
      print("TTS Rate limit reached - Fallback on Google text-to-speech")
      return save_gtts(text)

def save_gtts(text):
   tts = gTTS(text=text, lang='es')
   path = f"{AUDIO_PATH}{uuid.uuid4()}.mp3"
   tts.save(path)
   return path

def tts(context):
   translator = Translator()
   post = context["post"]
   post.title_audio = save_tts(translator.translate(post.title,src='en',dest='es').text)
   for comment in post.comments:
      comment.body_audio = save_tts(translator.translate(comment.body,src='en',dest='es').text)
      if comment.reply:
         comment.reply_audio = save_tts(translator.translate(comment.reply,src='en',dest='es').text)
   return

if __name__ == "__main__":
   save_tts("i am a potato")
