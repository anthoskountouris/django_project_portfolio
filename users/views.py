from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout # login authentication
from django.contrib.auth.decorators import login_required # decorator
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm # model forms
from django.contrib.auth.models import User # user model
from .models import Profile
from .forms import CustomUserCreationForm

# Create your views here.

def loginUser(request):
    page = 'login'

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
    messages.info(request, 'User was succesfully logged out!')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # save the instance before storing it to the db
            user.username = user.username.lower() # turn the username to lowercase
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user) # we login the user
            return redirect('profiles')
        
        else: 
            messages.success(request, 'An error has occurred during registration')

    context = {"page" : page, 'form': form}
    return render(request, 'users/login_register.html', context)

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
               "otherSkills" : otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile # Getting logged in users profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile' : profile, 'skills' : skills, 'projects' : projects}
    return render(request, 'users/account.html', context)