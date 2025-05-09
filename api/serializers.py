from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    class Meta:
        model = Review
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField() # Adds attribute to the serializer

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, object): # We always have to start our method with get
        reviews = object.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data