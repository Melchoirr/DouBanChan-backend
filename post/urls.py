from django.urls import path
from post.views import *

urlpatterns = [
    path("add_post/", add_post),
    path("like_post/", like_post),
    path("dislike_post/", dislike_post),
    path("post_set_favorite/", post_set_favorite),
    path("post_cancel_favorite/", post_cancel_favorite),
    path("query_single_post/", query_single_post),
    path("reply_post/", reply_post),
    path("query_group_posts/", query_group_posts),
    path("query_posts_by_tag/", query_posts_by_tag),
    path("query_posts_by_chat/", query_posts_by_chat)
]

