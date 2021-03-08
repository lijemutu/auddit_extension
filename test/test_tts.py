# Python code to demonstrate working of unittest 
import unittest 
from src.tasks.text_to_speech.task import save_tts, save_gtts, save_ttsService
  
class TestTTS(unittest.TestCase): 
      
    def setUp(self): 
        pass
  
    def test_normal(self): 
        #save_ttsService("soy una papa")
        save_tts("Soy una papa que huele a café con leche")
        #save_gtts("Soy una papa")
  
if __name__ == '__main__': 
    unittest.main() 
