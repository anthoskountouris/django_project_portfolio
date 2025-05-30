from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout # login authentication
from django.contrib.auth.decorators import login_required # decorator
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm # model forms
from django.contrib.auth.models import User # user model
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles

# Create your views here.

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.POST:
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User was succesfully logged in!')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
            return redirect('edit-account')
        
        else: 
            messages.success(request, 'An error has occurred during registration')

    context = {"page" : page, 'form': form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 6)
    context = {'profiles' : profiles, 'search_query': search_query, 'custom_range': custom_range}
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

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance = profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
        
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile # Associate skill with particular owner
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False) # saves the instance of the skill without the owner field
            skill.owner = profile # assigning the owner field
            skill.save()
            messages.success(request, 'Skill was added succesfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile # Associate skill with particular owner
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated succesfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted succesfully!')

        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile # Associate skill with particular owner
    messagesRequests = profile.messages.all()
    unreadCount = messagesRequests.filter(is_read=False).count()
    context = {'messages': messagesRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile # Associate skill with particular owner
    messagesRequests = profile.messages.get(id=pk)
    if messagesRequests.is_read == False:
        messagesRequests.is_read = True
        messagesRequests.save()
    context = {'message': messagesRequests}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recepient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recepient = recepient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Message was succesfully sent!')
            return redirect('user-profile', pk=recepient.id)
    
    context = {'recepient': recepient, 'form': form}
    return render(request, 'users/message_form.html', context,)