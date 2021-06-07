from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=100)
    isPepega = models.BooleanField(default=False)
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Token(models.Model):
    key = models.CharField(max_length= 1000)
    user = models.ForeignKey(User, related_name='token', on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.key
    
    
    
