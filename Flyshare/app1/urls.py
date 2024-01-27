from django.urls import path
from app1 import views

from app1.views import *

urlpatterns = [
    path('get-post/',views.getpostPage,name='get-post'),
    path('help/',views.helpPage,name='help'),
    path('post1/',views.Post,name='post'),
    path('postAPI/',PostModelAPIView.as_view()),
    path('postAPI/<int:id>/',PostModelAPIViewID.as_view()),
    # path('chat/messages/<int:user_id>/', views.user_chat_list, name='user_chat_list'),
    # path('chat/messages/<int:user_id>/<int:other_user_id>/', views.chat_messages, name='chat_messages'),
    # path('chats/', chat_view, name='chat_view'),
    #  path('filter-posts/', filter_posts_view, name='filter_posts'),
    # path('edit_profile/', views.edit_profile, name='edit_profile'),
    #  path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profilePage, name='profile'),
    path('edit_profile/', views.edit_profilePage, name='edit_profile'),
    path('change/', views.change_passwordPage, name='change_password_page'),
    path('chats/', views.home, name='home'),
    path('<int:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]