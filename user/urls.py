from django.urls import path
from user.views import *

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("logout/", logout),
    path("upload_profile/", upload_profile),
    path("chage_password", change_password),
    path("home/", get_user_page),
    path("get_user_brief/", get_user_brief),
    path("query_single/", query_single_user)
]
