from django.urls import path
from user.views import *

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("logout/", logout),
    path("uploadProfile/", upload_profile),
    path("home/", get_user_page),
]
