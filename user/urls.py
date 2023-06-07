from django.urls import path
from user.views import *

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("update_profile/", update_profile),
    path("update_password", update_password),
    path("update_email", update_email),
    path("query_single/", query_single_user),
    path("get_user_movie/", get_user_movie),
    path("get_user_series/", get_user_series),
    path("get_user_book/", get_user_book),
    path("get_user_fav_post/", get_user_fav_post),
    path("get_user_fav_text1/", get_user_fav_text1),
    path("get_self_post/", get_self_post),
    path("get_self_group/", get_self_group),
    path("change_profile/", change_profile),
    path("change_password/", change_password),
]
