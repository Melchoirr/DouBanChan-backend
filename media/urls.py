from django.urls import path
from media.views import *

urlpatterns = [
    path("create/", create_media),
    path("delete/", delete_media),
    path("query_single/", query_single_media),
    path("video_home/", media_home),
    path("set_watched/", set_watched),
    path("set_watching/", set_watching),
    path("set_to_be_watched/", set_to_be_watched),
    path("set_favourite/", set_favourite),
    path("comment_media/", comment_media),
]
