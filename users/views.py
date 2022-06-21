from .models import NewUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .serializers import RegisterUserSerializer, UserDataSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class CustomUserCreate(APIView):
    permission_class = [AllowAny]
    
    def post(self, request, format='json'):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response("User successfully created.", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#blacklist user on logout such that refresh token no longer works
class BlackListTokenView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
#gets username associated with request
class UserInfo(RetrieveAPIView):
    permission_class = [AllowAny]
    
    def get_user(self, email):
        return NewUser.objects.get(email=email)
    
    def get(self, request, email):
        
        #todo -- only allow to get account associated w/ own email
        user = self.get_user(email)
        if user is not None:
            content = { "user_name":user.user_name, "user_id":user.id }
            print(content)
            return Response(data=content, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    