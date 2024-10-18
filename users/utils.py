from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage # Separates our data into pages

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page') # getting the page number from the request
    # results = 3 results per page
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page) # reset profiles shown using the paginator
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    customRange = range(leftIndex, rightIndex)

    return customRange, profiles

def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'): # Searching for the query
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)    
        
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills) # Does the profile have a skill that's listed in this qurey set
        ) # We wrap the queries in Q

    return profiles, search_query