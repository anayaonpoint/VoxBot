from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model): 
 name = models.CharField(max_length=100)
 email = models.EmailField(max_length=100, unique=True)
 password = models.CharField(max_length=128) 

 def __str__(self) -> str:
  return self.name 
 

class History(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 query = models.CharField(max_length=255)
 created_at = models.DateTimeField(auto_now_add=True)

 def __str__(self):
  return self.query
  # accounts/models.py



class Journal(models.Model):
    content = models.TextField()
    mood = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mood} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"