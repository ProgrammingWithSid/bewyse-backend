"""bewyse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from users.view.login_view import login_view,register_view
from users.view.view_profile import view_profile,edit_user_profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/profile/view/', view_profile, name='view_profile'), 
    path('accounts/profile/edit/', edit_user_profile, name='edit_user_profile'), 

    
]
