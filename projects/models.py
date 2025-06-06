from django.db import models
import uuid #16 char string of numbers and letters
from users.models import Profile

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE) # many to one relationship
    title = models.CharField(max_length=200)
    description = models.TextField(null = True, blank=True) # Can leave it empty (database, django) to know
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length = 2000, null = True, blank = True)
    source_link = models.CharField(max_length = 2000, null = True, blank = True)
    tags = models.ManyToManyField('Tag', blank = True) # In string to be able to add it 
    vote_total = models.IntegerField(default = 0, null = True, blank = True)
    vote_ratio = models.IntegerField(default = 0, null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                          primary_key = True, editable = False)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title'] # ordering, use - infront for descending

    @property
    def imageUrl(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True) # Getting a single attribute of those reviews, flat converts that into a true list)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()
    

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True) # 1 - many
    project = models.ForeignKey(Project, on_delete = models.CASCADE) # If a project is deleted the reviews are deleted
    body = models.TextField(null = True, blank=True)
    value = models.CharField(max_length = 200, choices = VOTE_TYPE)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                          primary_key = True, editable = False)
    
    class Meta:
        # Binding owner and project so that a user can only have one review on a project
        unique_together = [['owner', 'project']]
    
    def __str__(self):
        return self.value
    

class Tag(models.Model):
      # owner = 
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique = True, 
                          primary_key = True, editable = False)
    
    def __str__(self):
        return self.name
    