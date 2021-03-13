import uuid
import time
import requests
import random
from gtts import gTTS
from googletrans import Translator
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, languageconfig, ResultReason, CancellationReason
from azure.cognitiveservices.speech.audio import AudioOutputConfig


VOICES = ["Matthew", "Joey", "Kendra"] # English voices
VOICES = ["Mia"] # Spanish voice
AUDIO_PATH = "data/audio/"
TTSMP3_URL = "https://ttsmp3.com/makemp3_new.php"


def save_tts(text):
   time.sleep(random.uniform(1,3))
   try:
      filename = uuid.uuid4()
      path = f"{AUDIO_PATH}{filename}.mp3"
      speech_config = SpeechConfig(subscription="e1b1739b0039424cb6f0cbb39def283a",\
          region="southcentralus")
      audio_config = AudioOutputConfig(filename=path)

      synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

      text = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="es-MX">
        <voice name="es-MX-HildaRUS">
            {text}            
        </voice>
    </speak>""" 

      ## Calling the Speech Sythesizer 
      result = synthesizer.speak_ssml_async(ssml=text).get()

      if result.reason == ResultReason.SynthesizingAudioCompleted:
         pass
      #   print("Speech synthesized to speaker for text [{}]".format(text))
      elif result.reason == ResultReason.Canceled:
         cancellation_details = result.cancellation_details
         print("Speech synthesis canceled: {}".format(cancellation_details.reason))
         if cancellation_details.reason == CancellationReason.Error:
            if cancellation_details.error_details:
               raise Exception("Error details: {}".format(cancellation_details.error_details))
         print("Did you update the subscription info?")

      return path
   except:
      print("TTS Rate limit reached - Fallback on Google text-to-speech")
      return save_ttsService(text)

def save_ttsService(text):
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
   post = context["post"]
   post.title_audio = save_tts(post.title)
   for comment in post.comments:
      comment.body_audio = save_tts(comment.body)
      
   return

if __name__ == "__main__":
   save_tts("i am a potato")
