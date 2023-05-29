from django.urls import path
from text.views import *

urlpatterns = [
    path("query_single/", query_single_text),
    path("reply/", reply_text),
    path("delete/", delete_text),
    path("like/", like_text),
    path("dislike/", dislike_text),
]
