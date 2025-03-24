from django.forms import ModelForm
from django import forms # adding this to customize the form
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta: 
        model = Project # name of model
        # fields = '__all__' # fields from the model to add on the form
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link']
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'class' : 'input', 'placeholder': 'Add title' })

        for name,field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'})
        # self.fields['description'].widget.attrs.update({'class' : 'input', 'placeholder': 'Add description' })

        # self.fields['demo_link'].widget.attrs.update({'class' : 'input', 'placeholder': 'Add demo link' })

        # self.fields['demo_link'].widget.attrs.update({'class' : 'input', 'placeholder': 'Add demo link' })


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body'] 

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'})
    