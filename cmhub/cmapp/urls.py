from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [

    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='cmapp/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='cmapp/index.html'), name="logout"),
    path('edit_profile/', views.edit_profile,name='edit_profile'),
    url(r'^delete_user/(?P<pk>.*)', views.delete_user, name='delete_user'),
    url(r'create_post/(?P<owner>.*)', views.create_post,name='create_post'),
    path('display_posts/', views.display_posts,name='display_posts'),
    url(r'^delete_post/(?P<pk>.*)', views.delete_post, name='delete_post'),
    url(r'^edit_post/(?P<idpost>.*)', views.edit_post, name='edit_post'),
    url(r'^display_post/(?P<pk>.*)', views.display_post, name='display_post'),
]