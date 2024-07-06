from django.shortcuts import render # Allow us to render the templates
from django.http import HttpResponse
from .models import Project

projectsList = [
    {'id':'1',
     'title':"Ecommerce Website",
     'description': 'Fully functional ecommerce website'
     },
     {'id':'2',
     'title':"Portfolio Website",
     'description': 'This was a project I built out my portfolio'
     },
     {'id':'3',
     'title':"Social Network",
     'description': 'Awesome open source project I am still working on'
     }
]

def projects(request):
    projects = Project.objects.all()
    context = {'projects' : projects}
    # return HttpResponse("Here are our projects")
    return render(request, 'projects/projects.html', context)
    

def project(request, pk):
    projectsObj = Project.objects.get(id=pk)
    context = {'project' : projectsObj}
    return render(request, 'projects/single-project.html', context)
