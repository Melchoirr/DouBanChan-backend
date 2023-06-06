from django.urls import path
from post.views import *

urlpatterns = [
    path("like_post/", like_post),
    path("dislike_post/", dislike_post),
    path("post_set_favorite/", post_set_favorite),
    path("query_single/", query_single_post),
    path("reply_post/", reply_post),
]

