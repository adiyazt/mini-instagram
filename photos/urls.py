from django.contrib import admin
from django.urls import path
from .views import (register, login, api_auth, 
                    api_reg, users, deauth, index,
                    post_photo, api_dislike, api_like, comments
                    )

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('user/', users, name='user'),
    path('deauth/', deauth, name='deauth'),
    path('api/v1/authorization', api_auth, name='api_login'),
    path('api/v1/registration', api_reg, name='api_register'),
    path('post_photo/', post_photo, name='post_photo'),
    path('api/v1/like/<str:photo_id>', api_like, name='api_like'),
    path('api/v1/dislike/<str:photo_id>', api_dislike, name='api_dislike'),
    path('comments/<str:photo_id>', comments, name='comments')
    
]
