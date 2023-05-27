from django.urls import path
from post.views import *

urlpatterns = [
    path("like_post/", like_post),
    path("dislike_post/", dislike_post),
]

