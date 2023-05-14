from django.urls import path
from group.views import *


urlpatterns = [
    path("cerate/", create_group),
    path("delete/", delete_group),
    path("query_single/", query_single_group),
]
