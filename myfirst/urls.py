"""
URL configuration for myfirst project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# project-level urls.py

from django.contrib import admin
from django.urls import path, include
from articles import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.homepage, name='homepage'),
    path('grappelli/', include('grappelli.urls')),
    path("admin/", admin.site.urls),
    path('articles/', include('articles.urls')),
    path('register/',views.register, name = 'register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/user_create_article', views.user_create_article, name='user_create_article'),
    path('update-profile/', views.update_profile, name='update_profile'),

]
