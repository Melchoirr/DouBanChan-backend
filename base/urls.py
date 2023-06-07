from django.urls import path
from base.views import *

urlpatterns = [
    path("query_base/", query_base),
    path("query_user/", query_user),
    path("query_chat/", query_chat),
    path("query_post/", query_post),
    path("query_group/", query_group),
    path("query_media/", query_media),
    path("base_movie_series_list/", base_movie_series_list),
    path("base_book_list/", base_book_list),
    path("col_media_series/", col_media_series),
    path("col_book/", col_book),
]
