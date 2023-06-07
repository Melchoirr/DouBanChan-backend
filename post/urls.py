from django.urls import path
from post.views import *

urlpatterns = [
    path("add_post/", add_post),
    path("get_post_status1/", get_post_status1),
    path("like_post/", like_post),
    path("cancel_like_post/", cancel_like_post),
    path("cancel_dislike_post/", cancel_dislike_post),
    path("dislike_post/", dislike_post),
    path("post_set_favorite/", post_set_favorite),
    path("post_cancel_favorite/", post_cancel_favorite),
    path("query_single_post/", query_single_post),
    path("reply_post/", reply_post),
    path("delete_post/", delete_post),
    path("set_essence/", set_essence),
    path("set_top/", set_top),
    path("cancel_essence/", cancel_essence),
    path("cancel_top/", cancel_top),
    path("query_group_posts/", query_group_posts),
    path("query_posts_by_tag/", query_posts_by_tag),
    path("query_posts_by_chat/", query_posts_by_chat)
]

