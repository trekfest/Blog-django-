from django.contrib.auth.models import User
import datetime
from django.db import models
from django.utils import timezone
from django.db import models



class Article(models.Model):
    article_title = models.CharField('Name of the text', max_length=255)
    article_text = models.TextField('Text')
    pub_date = models.DateTimeField('Date of the publication', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=7))

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_name = models.CharField('Author', max_length=50)
    comment_text = models.CharField('Comment', max_length=200)

    def __str__(self):
        return self.author_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    

    def __str__(self):
        return self.user.username


