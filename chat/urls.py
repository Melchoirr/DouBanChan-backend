from django.urls import path
from chat.views import *


urlpatterns = [
    path("create/", create_chat),
    path("delete/", delete_chat),
    path("query_single/", query_single_chat),
    path("chat_home/", chat_home),
    path("join_chat/", join_chat),
    path("quit_chat/", quit_chat),
    path('add_post/', add_post),
    path('reply_post/', reply_post),
    path('delete_post/', delete_post),
    path("like_post/", like_post),
    path("dislike_post/", dislike_post),

]
