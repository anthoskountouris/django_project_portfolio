from django.db.models.signals import post_save # This signal is gonna trigger every time the model is saved  already 
from django.db.models.signals import post_delete # This signal is gonna trigger every time an isntance is deleted 

from django.dispatch import receiver # decorator
from django.contrib.auth.models import User
from .models import Profile

from django.core.mail import send_mail
from django.conf import settings

# @receiver(post_save, sender=Profile) # Added the receiver
def createProfile(sender, instance, created, **kwargs): 
    print("Profile signal triggered!")
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = 'Welcome to DevSearch'
        message = 'We are glad you are here!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    print("Delete user signal triggered!")
    user = instance.user # it's .user because that's how we get a 1-1 relationship
    user.delete()

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile) # After our ptofile is updated we want to update the used.
post_delete.connect(deleteUser, sender=Profile)