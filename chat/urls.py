from django.urls import path
from chat.views import *


urlpatterns = [
    path("create/", create_chat),
    path("delete/", delete_chat),
    path("query_single/", query_single_chat),
    path("chat_brief/", chat_brief),
    path("join_chat/", join_chat),
    path("quit_chat/", quit_chat),
    path("query_free_chat/", query_free_chat),
    path("query_chat_by_group/", query_chat_by_group),
    path("query_chat_by_tag/", query_chat_by_tag),
    path("query_chat_by_heat/", query_chat_by_heat)
]
