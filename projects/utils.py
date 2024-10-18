from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage # Separates our data into pages

def paginateProjects(request, projects, results):
    page = request.GET.get('page') # getting the page number from the request
    # results = 3 results per page
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page) # reset projects shown using the paginator
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    customRange = range(leftIndex, rightIndex)

    return customRange, projects

def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)    
    
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) | # We go into the parent object of owner to get the names of profiles
        Q(tags__in=tags)
    )   

    return projects, search_query