from django.urls import path
from post.views import *

urlpatterns = [
    path("like_post/", like_post),
    path("dislike_post/", dislike_post),
    path("query_single/", query_single_post),
    path("add_text/", add_text),
]

