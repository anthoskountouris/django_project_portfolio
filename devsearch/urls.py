"""
URL configuration for devsearch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings # we want access to our setting file to find the media root and url
from django.conf.urls.static import static # It's going to heko us create a url for the static file

from django.contrib.auth import views as auth_views # password reset

urlpatterns = [
    path('admin/', admin.site.urls), # We cannot access it until we have the database ready
    path('projects/', include('projects.urls')),
    path('', include('users.urls')),
    path('api/', include('api.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name = "password_reset"), # user submits emai for reset

    path('reset_pasword_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name = "password_reset_done"), # Email sent message

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),
         name = "password_reset_confirm"), # Email with link and reset instructions

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name = "password_reset_complete"), # Password succesfully reset message

    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
