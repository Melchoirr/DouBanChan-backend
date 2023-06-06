from django.urls import path
from media.views import *

urlpatterns = [
    path("create/", create_media),
    path("delete/", delete_media),
    path("query_single/", query_single_media),
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
    path("get_preview/", get_media_preview),
    path("get_heat_comment/", get_heat_comment),
    path("get_heat_movie/", heated_movie),
    path("get_heat_series/", heated_series),
    path("related_group/", related_group),
    path("related_chat/", related_chat),
]
