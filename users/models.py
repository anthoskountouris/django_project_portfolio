from django.db import models
from django.contrib.auth.models import User
import uuid #16 char string of numbers and letters



# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null = True)
    email = models.EmailField(max_length=500, blank=True, null = True)
    username = models.CharField(max_length=200, blank=True, null = True)
    location = models.CharField(max_length=200, blank=True, null = True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, blank=True, null = True)
    social_twitter = models.CharField(max_length=200, blank=True, null = True)
    social_linkedin = models.CharField(max_length=200, blank=True, null = True)
    social_youtube = models.CharField(max_length=200, blank=True, null = True)
    social_website = models.CharField(max_length=200, blank=True, null = True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                          primary_key = True, editable = False)
    
    
    def __str__(self):
        return str(self.username)
    
    class Meta:
        ordering = ['created']
    
    @property
    def imageUrl(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url
    

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null = True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                          primary_key = True, editable = False)
    
    def __str__(self):
        return str(self.name)
    

# receiver of signal:
# sender is gonna be the model that actually sends this
# instance of the model that triggers this
# created will let us know of the user was added, or if a model was added to the db

class Message(models.Model):
    # If we send a message to someone and delete our account, the recepientcan still see the message, form can be submitted without a sender 
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True) 
    recepient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages") # we set this to messages so that it would know which is what 
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                          primary_key = True, editable = False)
    
    
    def __str__(self):
        return str(self.subject)
    
    class Meta:
        ordering = ['is_read', '-created'] #false values will be at the top, then by the created value
    