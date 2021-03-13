class Post:
   def __init__(self, title, comments):
      self.title: str = title
      self.comments: [Comment] = comments

   def __str__(self):
      s = f"{self.title}\n"
      for c in self.comments:
         s += f"\n{c}"
      return s
   def __copy__(self):
        return Post(self.title,self.comments)

class Comment:
   def __init__(self, body, reply):
      self.body: str = body
      self.reply: str = reply

   def __str__(self):
      return f"{self.body}\n\t{self.reply}"
