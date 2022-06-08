from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from blog.models import Post, Comment
from django.contrib.auth.models import User

# Create your tests here.

#automatic testing
#run with coverage run --omit='/*venv/*' manage.py test
#print results with coverage html
#more with model testing 

class PostTests(APITestCase):
    
    #tests if data can be viewed   
    def test_view_posts(self):
        url = reverse('blogapi:post_list')
        response = self.client.get(url, format='json')  #simulates client sending a request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
     
    #tests if data can be created    
    def test_create_post(self):
        self.testuser1 = User.objects.create_user(username='test', password='123456789')
        data = {"title": "new", "author":1, "content":"new"}
        url = reverse('blogapi:post_list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_post_update(self):
        client = APIClient()
        testuser1 = User.objects.create_user(username='test_user1', password='123456789')
        testuser2 = User.objects.create_user(username='test_user2', password='123456789')
        test_post = Post.objects.create(author_id = 1)
        
        #test that post author can edit
        client.login(username=testuser1.username, password='123456789')
        url = reverse(('blog_api:post_details'), kwargs={'pk':1})
        response = client.put(
            url, {
                "title": "new",
                "content" : "new",
                "author" : 1,
                "status": "published"
            }, format='json')
        result = response.status_code != status.HTTP_200_OK
        if result:
            print(response.data)
            self.assertEqual(False)
        
        #test that other users cannot edit
        client.logout()
        client.login(username=testuser2.username, password='123456789')
        response = client.put(
            url, {
                "title": "new",
                "content" : "new1",
                "author" : 2,
                "status": "published"
            }, format='json')
        result = response.status_code != status.HTTP_400_BAD_REQUEST
        if result:
            print(response.data)
            self.assertEqual(False)
    
    #tests if data can be viewed   
    def test_comment_view(self):
        url = reverse('blogapi:comment_list')
        response = self.client.get(url, format='json')  #simulates client sending a request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
     
    #tests if data can be created    
    def test_comment_create(self):
        self.testuser1 = User.objects.create_user(username='test', password='123456789')
        test_post = Post.objects.create(author_id = 1)
        data = {"parent_post" : 1, "author": 1, "content":"new"}
        url = reverse('blogapi:comment_list')
        response = self.client.post(url, data, format='json')
        result = response.status_code != status.HTTP_201_CREATED
        if result:
            print(response.data)
            self.assert_(False)
            
    def test_comment_update(self):
        client = APIClient()
        testuser1 = User.objects.create_user(username='test_user1', password='123456789')
        testuser2 = User.objects.create_user(username='test_user2', password='123456789')
        test_post = Post.objects.create(author_id = 1)
        test_comment = Comment.objects.create(author_id = 1, parent_post_id = 1)
        test_comment2 = Comment.objects.create(author_id = 1, parent_post_id = 1)
        test_comment3 = Comment.objects.create(author_id = 1, parent_post_id = 1)
        
        #test that post author can edit
        client.login(username=testuser1.username, password='123456789')
        url = reverse(('blog_api:comment_details'), kwargs={'pk':1})
        response = client.put(
            url, {
                "author" : 1,
                "parent_post" : 1,
                "content" : "new"
            }, format='json')
        result = response.status_code != status.HTTP_200_OK
        if(result):
            print(response.data)
            self.assertEqual(result)
        
        #test that other users cannot edit
        client.logout()
        client.login(username=testuser2.username, password='123456789')
        response = client.put(
            url, {
                "author" : 1,
                "parent_post" : 1,
                "content" : "new"
            }, format='json')
        result = response.status_code != status.HTTP_400_BAD_REQUEST
        if(result):
            print(response.data)
            self.assertEqual(result)
            
    def test_post_commentlist_view(self):
        client = APIClient()
        testuser1 = User.objects.create_user(username='test_user1', password='123456789')
        test_post = Post.objects.create(author_id = 1)

        #test post with no comments does not display comments
        client.login(username=testuser1.username, password='123456789')
        url = reverse(('blog_api:post_commentlist'), kwargs={'pk':1})
        response = self.client.get(url, format='json')  #simulates client sending a request
        result = (response.status_code, status.HTTP_404_NOT_FOUND)
        if(result[0] != result[1]):
            print(response.data)
            self.assertEqual(result[0], result[1])
            
        test_comment = Comment.objects.create(author_id = 1, parent_post_id = 1)
        test_comment2 = Comment.objects.create(author_id = 1, parent_post_id = 1)
        test_comment3 = Comment.objects.create(author_id = 1, parent_post_id = 1)
        
        response = self.client.get(url, format='json')  #simulates client sending a request
        result = (response.status_code, status.HTTP_200_OK)
        if(result[0] != result[1]):
            print(response.data)
            self.assertEqual(result[0], result[1])