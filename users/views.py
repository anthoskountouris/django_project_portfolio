from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout # login authentication
from django.contrib.auth.decorators import login_required # decorator
from django.contrib import messages
from django.contrib.auth.models import User # user model
from .models import Profile

# Create your views here.

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')



        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User was succesfully logged in!')
            return redirect('profiles')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'User was succesfully logged out!')
    return redirect('login')

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles' : profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="") # Excludes the skills with no description
    otherSkills = profile.skill_set.filter(description="") # Filters the skills with an empty description

    context = {'profile' : profile,
               "topSkills" : topSkills,
               "otherSkills": otherSkills}
    return render(request, 'users/user-profile.html', context)