from django.urls import path
from .views import CustomUserCreate, BlackListTokenView, UserInfo

app_name = 'users'

urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name="create_user"),
    path('logout/blacklist/', BlackListTokenView.as_view(), name="blacklist"),
    path('info/<str:email>', UserInfo.as_view(), name="user_info"),
]