from django.shortcuts import render, redirect # Allow us to render the templates
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag # Adding the model
from .forms import ProjectForm, ReviewForm # Adding the forms
from .utils import searchProjects, paginateProjects

# projectsList = [
#     {'id':'1',
#      'title':"Ecommerce Website",
#      'description': 'Fully functional ecommerce website'
#      },
#      {'id':'2',
#      'title':"Portfolio Website",
#      'description': 'This was a project I built out my portfolio'
#      },
#      {'id':'3',
#      'title':"Social Network",
#      'description': 'Awesome open source project I am still working on'
#      }
# ]

def projects(request):
    projects, search_query = searchProjects(request)
    customRange, projects = paginateProjects(request, projects, 6) # number of results we want
    context = {'projects' : projects, 'search_query': search_query, 'customRange' : customRange}
    return render(request, 'projects/projects.html', context)
    

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    reviews = projectObj.review_set.all
    form = ReviewForm() ## instansiate the form

    if request.method == 'POST': 
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        if form.is_valid(): # We check if the data and form are validate
            form.save()
        
        projectObj.getVoteCount # getting votes
        
        messages.success(request, 'Your review was successfullt submitted')
        return redirect('project', pk=projectObj.id)

    context = {'project' : projectObj, "reviews": reviews, 'form': form}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login") 
def updateProject(request, pk):
    profile = request.user.profile # we get the profile of the logged in user
    project = profile.project_set.get(id=pk) # we are querying only that users projects, we are getting all the chldren/projects

    form = ProjectForm(instance=project) ## instansiate the form

    # We check what method it was
    if request.method == 'POST':
        newtags:list[str] = request.POST.get('newtags').replace(','," ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        # print(request.POST)
        if form.is_valid(): # We check if the data and form are validate
            project = form.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag) # if tag already exists don't add it
                project.tags.add(tag) # accessing the many to many relationship
            return redirect('account')
        

    context = {'form' : form, 'project': project}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login") 
def createProject(request):
    profile = request.user.profile

    form = ProjectForm() ## instansiate the form

    # We check what method it was
    if request.method == 'POST':
        newtags:list[str] = request.POST.get('newtags').replace(','," ").split()

        form = ProjectForm(request.POST, request.FILES)
        # print(request.POST)
        if form.is_valid(): # We check if the data and form are validate
            project = form.save(commit = False) # Gives us an instance of the current project and then we can go and update that project attribure
            project.owner = profile # and then we can go and update that project attribure
            project.save() # and then we save again
        
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag) # if tag already exists don't add it
                project.tags.add(tag) # accessing the many to many relationship
                
            return redirect('account')
        

    context = {'form' : form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login") 
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('account')
    
    context = {'object':project}
    return render(request, 'delete_template.html', context)