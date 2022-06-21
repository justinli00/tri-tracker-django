from blog.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly, IsAuthenticated

#permission classes
class UserPermission(BasePermission):
    post_message = "Only the author of this post may modify it."
    comment_message = "Only the author of this comment may modify it."
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return obj.author == request.user
        

#gets all PUBLISHED posts -- ignores draft posts
class PostList(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]    
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer

    #overloaded to allow for unauthorized users to read
    def get(self, request, format=None):
        return self.list(request, format)

    #overloaded debugging methods with prints
    def post(self, request, format=None):
        if request.auth is None:
            return Response("PostList: to use POST method, user must be authenticated.", status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#gets one specific post, based on id
class PostDetail(generics.RetrieveUpdateDestroyAPIView, UserPermission):
    permission_classes = [UserPermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    #this doesn't override the GET method (duh)
    def get_post(self, pk):
        return Post.objects.get(pk=pk)
    def put(self, request, pk, format=None):  
        serializer = PostSerializer(self.get_post(pk), data=request.data)
        if serializer.is_valid():
            #check for validation
            obj = Post.objects.get(pk=pk)
            if UserPermission.has_object_permission(self, request, PostDetail, obj) == False:
                return Response(UserPermission.post_message, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("PostDetail.put:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#gets all comments        
class CommentList(generics.ListCreateAPIView):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

#gets all comments for a given post   
#does not allow posting, since there's no elegant way to ensure that incoming comment has correct parent post (that I know of) 
class PostCommentList(generics.ListAPIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]    
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    def get_post_id(self, pk):
        return Post.objects.get(pk=pk).id
    
    def get(self, request, pk):
        #get parent post
        comments = Comment.objects.all().filter(parent_post=self.get_post_id(pk))
        if comments.exists() == False:
            #post has no comments
            return Response("This post has no comments.", status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
#gets all comments for a given post    
class CommentDetails(generics.RetrieveUpdateDestroyAPIView, UserPermission):
    permission_classes = [UserPermission]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    #this doesn't override the GET method (duh)
    def get_comment(self, pk):
        return Comment.objects.get(pk=pk)
    
    def put(self, request, pk, format=None):      
        serializer = CommentSerializer(self.get_comment(pk), data = request.data)
        if serializer.is_valid():
            #check for validation
            obj = Comment.objects.get(pk=pk)
            if UserPermission.has_object_permission(self, request, CommentDetails, obj) == False:
                return Response(UserPermission.comment_message, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("CommentDetail.put:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)