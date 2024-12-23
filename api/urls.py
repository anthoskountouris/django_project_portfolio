from django.urls import path
from . import views

# Generates a json web token for the user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Generates a single token
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Generates a refresh token

    path('', views.getRoutes),
    path('projects', views.getProjects),
    path('projects/<str:pk>', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),
]