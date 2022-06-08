from rest_framework import serializers
from blog.models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'image', 'author', 'content', 'status',
                  'activity_start', 'activity_end', 'activity_distance', 'distance_units', 'activity_type',)
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'published', 'author', 'parent_post', 'content',)