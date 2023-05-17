from django.urls import path
from chat.views import *


urlpatterns = [
    path("create/", create_chat),
    path("delete/", delete_chat),
    path("query_single/", query_single_chat),
]
