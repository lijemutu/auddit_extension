# Python code to demonstrate working of unittest 
import unittest ,json
from src.tasks.generate_thumbnail.task import generate_thumbnail

class Post:
    pass
  
class TestThumbnail(unittest.TestCase): 
      
    def setUp(self): 
        pass
  
    def test_normal(self): 
        post = Post()
        post.title = "a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a "
        post.score = 42069
        post.num_comments = 42069
        pageName ='eli5'
        with open('doc/'+pageName+'.json') as page:
            page = json.load(page)
            ctx = {
                "subreddit": "askreddit",
                "post": post,
                "video_id": "test",
                "page":page
            }
            generate_thumbnail(ctx)
  
if __name__ == '__main__': 
    unittest.main() 
