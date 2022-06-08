from .models import Post
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status

#automatic testing
#run with >coverage run --omit='/*venv/*' manage.py test
#print results with coverage html
#more with model testing 

class Test_Create_Post(TestCase):
    
    #creates a dummy database for tests to run on
    @classmethod
    def setUpTestData(cls): 
       testuser1 = User.objects.create_user(username='test_user1', password='123456789')
       test_post = Post.objects.create(title='foo', slug='f', author_id=1, status='published', content='c')
       
    def test_blog_content(self):
        post = Post.postobjects.get(id=1)
        author = f'{post.author}'
        title = f'{post.title}'
        content = f'{post.content}'
        status = f'{post.status}'
        self.assertEqual(author, 'test_user1')
        self.assertEqual(title, 'foo')
        self.assertEqual(status, 'published')
        self.assertEqual(content, 'c')
        self.assertEqual(str(post), 'foo')        
        