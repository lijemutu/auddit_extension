import praw
import os,requests,uuid
from praw.models import MoreComments
from .post import Post, Comment
import prawcore,time,json
from googletrans import Translator

client_id = "JQYTt6OcPBrlqg"
client_secret = "O617WeQTJ9hGHwgK3h5zhWAUKHvVuw"

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent='contentGet',username='erlototo',password='lijemutu2112')
def isPostDuplicate(context,post):
   page = context['page']
   used_post = page['used_post']
   return post.permalink in used_post

def addPost(context,post):
   context['page']['used_post'].append(post.permalink)
   with open(context['page']['location'],'w') as f:
      f.write(json.dumps(context['page']))
   return 
   
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

def spanishTranslateAzure(text):
   time.sleep(10)
   subscriptionAzure="e1b1739b0039424cb6f0cbb39def283a"
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
   request = requests.post(constructed_url, params=params, headers=headers, json=text)
   response = request.json()
   return response



def previewPost(post):
   i = 0
   print(f"Post name: {post.title}")
   for comment in post.comments:
      print(f"Comment {i}: {comment.body}")
      i+=1
   decide = str(input("Do you want to skip post(P) or comments(C) or nah(N)\n")).upper()
   #decide = 'C'
   if decide == 'N':
      return
   if decide == 'P':
      return 0
   if decide == 'C':
      deleted_comments = [int(item) for item in input("Select deleted comments : ").split()]
      #deleted_comments = [0,2]
       
      for index in sorted(deleted_comments, reverse=True):
         del post.comments[index]


def get_hottest_post(context):
   subreddit_name=context["subreddit"]
   comment_limit=context["comment_limit"]
   nsfw=context["nsfw"]
   subreddit = reddit.subreddit(subreddit_name)
   hot_posts = subreddit.hot(limit=100)
   
   
   while True:
      try:
         for post in hot_posts:
            chars = ''
            if isPostDuplicate(context,post):
               continue
            if not post.stickied and post.over_18 == nsfw:
               title = post.title
               chars+=title
               comments = []
               for comment in post.comments:
                  if isinstance(comment, MoreComments):
                     continue
                  if comment.stickied:
                     continue
                  if comment.edited:
                     continue
                  if len(comment.body) > 2000:
                     continue
                  if 'http' in comment.body:
                     continue
                  comment_body = comment.body
                  chars+=comment_body
                  if comment_body == "[removed]":
                     continue
                  comment_reply = ""
                  comment.replies.replace_more(limit=1)
                  if len(comment.replies) > 0:
                     reply = comment.replies[0]
                     if isinstance(reply, MoreComments):
                        continue
                     comment_reply = reply.body
                     chars+=comment_reply
                  comment_output = Comment(comment_body, comment_reply)
                  comment_output.author = comment.author.name
                  comment_output.score = comment.score
                  comments.append(comment_output)
                  if len(comments) >= comment_limit:
                     break
               
               post_data = Post(title, comments)
               post_data.score = post.score
               post_data.num_comments = post.num_comments
               post_data.permalink = post.permalink

               post_data = translatePosts(post_data)
               
               if  previewPost(post_data) == 0:
                  continue
               context["post"] = post_data            
               addPost(context,post)
               print("Post name: ",title," char len: ",len(chars))
               break
            

      except prawcore.exceptions.RequestException:
               print(f"Retrying: get hottest post")
               time.sleep(5)
               continue
      break
   return


if __name__ == '__main__':

   get_hottest_post()
