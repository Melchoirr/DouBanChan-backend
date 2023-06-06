from django.urls import path
from user.views import *

urlpatterns = [
    path("register/", register),
    path("login/", login),
    # path("logout/", logout),
    path("update_profile/", update_profile),
    path("update_password", update_password),
    path("update_email", update_email),
    path("query_single/", query_single_user)
]
