from django.urls import path
from text.views import *

urlpatterns = [
    path("query_single/", query_single_text),
    path("reply/", reply_text),
    path("delete/", delete_text),
    path("like/", like_text),
    path("cancel_like/", cancel_like_text),
    path("dislike/", dislike_text),
    path("cancel_dislike/", cancel_dislike_text),
    path("text_cancel_favorite/", text_cancel_favorite),
    path("text_set_favorite/", text_set_favorite),
]
