from django.urls import path
from chat.views import *


urlpatterns = [
    path("create/", create_chat),
    path("delete/", delete_chat),
    path("query_single/", query_single_chat),
    path("chat_home/", chat_home),
    path("join_chat/", join_chat),
    path("quit_chat/", quit_chat),
]
