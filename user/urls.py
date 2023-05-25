from django.urls import path
from user.views import *

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("logout/", logout),
    path("upload_profile/", upload_profile),
    path("chage_password", change_password),
    path("query_single/", query_single_user)
]
