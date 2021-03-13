import time
from googletrans import Translator
import requests,uuid

def spanishTranslateAzure(text):
   time.sleep(2)
   subscriptionAzure="07d815d334e24017a39e761b2a5c3e08"
   endpoint = "https://api.cognitive.microsofttranslator.com"
   region="southcentralus"
   path = '/translate'
   constructed_url = endpoint + path
   params = {
    'api-version': '3.0',
    'from': 'en',
    'to': 'es'
   }
   headers = {
    'Ocp-Apim-Subscription-Key': subscriptionAzure,
    'Ocp-Apim-Subscription-Region': region,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
   }
   body = [{'text':text}]
   request = requests.post(constructed_url, params=params, headers=headers, json=body)
   response = request.json()
   return response[0]['translations'][0]['text']


def translatePosts(post):
   post.title = spanishTranslateAzure(post.title)
   for comment in post.comments:
      comment.body = spanishTranslateAzure(comment.body)
   return post

def spanishTranslate(text):

   time.sleep(10)
   translator = Translator()
   text = translator.translate(text,src='en',dest='es')
   if text._response.status_code == 429:
      raise Exception('Google translator has too many requests error code 429')

   return text.text