from .models import Profile, Skill
from django.db.models import Q


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