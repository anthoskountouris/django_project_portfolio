from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project

# All the routes that we're gonna have in our api
'''Json web tokens have an expiration date so when a user's token expires
which could be 5 minutes, we need to make sure that tey can stay logged in'''
@api_view(['GET'])  # We specify our method (decorator)
def getRoutes(request):

    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'}, # generate a token for the users to login
        {'POST':'/api/users/token'}, # refresh token

    ]

    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True) # This turns our python data and converts it into json data
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id = pk)
    serializer = ProjectSerializer(project, many=False) # This turns our python data and converts it into json data
    return Response(serializer.data)
