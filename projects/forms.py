from django.forms import ModelForm
from .models import Project


class ProjectForm(ModelForm):
    class Meta: 
        model = Project # name of model
        # fields = '__all__' # fields from the model to add on the form
        fields = ['title', 'description', 'demo_link', 'source_link', 'tags']