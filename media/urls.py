from django.urls import path
from media.views import *

urlpatterns = [
    path("create/", create_media),
    path("delete/", delete_media),
    path("query_single/", query_single_media),
    path("media_home/", media_home),
    path("set_watched/", set_watched),
    path("set_watching/", set_watching),
    path("set_to_be_watched/", set_to_be_watched),
    path("set_favourite/", set_favourite),
    path("comment_media/", comment_media),
    path("delete_comment", delete_comment),
    path("rate_media/", rate_media),
    path("like_comment/", like_comment),
    path("dislike_comment/", dislike_comment),
    path("filter/", media_filter),
    path("add_preview/", add_preview),
]
