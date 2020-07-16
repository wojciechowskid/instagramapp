"""instapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from instagram import views
from rest_framework.routers import DefaultRouter
from users.api import (UserViewSet)
from instagram.api import CreateInstagramAccountViewSet


router = DefaultRouter()
router.register(r'api/users', UserViewSet)

instagram_view = CreateInstagramAccountViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy'
})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth-window/', views.view),
    path('api/users/<int:user_id>/instagram/', instagram_view),
    path('', include(router.urls)),
]
