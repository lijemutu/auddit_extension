# Python code to demonstrate working of unittest 
import unittest 
from src.tasks.scrape_reddit.task import spanishTranslateAzure
from src.tasks.text_to_speech.task import save_tts
  
class TestAzureServices(unittest.TestCase): 

    def test_translate(self):
        text = 'We are translating from english to spanish'
        translated_text = spanishTranslateAzure(text)
        print(translated_text)

    def test_ttsAzure(self):
        text = 'Estamos leyendo en voz alta usando el servicio de Azure'
        path = save_tts(text)
        print(path)