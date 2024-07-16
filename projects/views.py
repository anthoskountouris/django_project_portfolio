from django.shortcuts import render, redirect # Allow us to render the templates
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project # Adding the model
from .forms import ProjectForm # Adding the form

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
    projects = Project.objects.all()
    context = {'projects' : projects}
    # return HttpResponse("Here are our projects")
    return render(request, 'projects/projects.html', context)
    

def project(request, pk):
    projectsObj = Project.objects.get(id=pk)
    context = {'project' : projectsObj}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login") 
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project) ## instansiate the form

    # We check what method it was
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        # print(request.POST)
        if form.is_valid(): # We check if the data and form are validate
            form.save()
            return redirect('projects')
        

    context = {'form' : form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login") 
def createProject(request):
    form = ProjectForm() ## instansiate the form

    # We check what method it was
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        # print(request.POST)
        if form.is_valid(): # We check if the data and form are validate
            form.save()
            return redirect('projects')
        

    context = {'form' : form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login") 
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {'object':project}
    return render(request, 'projects/delete_template.html', context)