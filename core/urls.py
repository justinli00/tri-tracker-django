"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import urls
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blogapi.urls', namespace='blogapi')),                     #api calls
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),   
    path('', include('blog.urls', namespace='blog')),      
    path('doc/', get_schema_view(
            title = 'Project Schema',
            description = "The schema for the project", 
            version="1.0.0"),
         name='openapi-schema'
        ),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', include('users.urls', namespace='users')),                    #user management
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
