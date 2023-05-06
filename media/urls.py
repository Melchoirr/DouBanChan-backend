from django.urls import path
from media.views import *


urlpatterns = [
    path("create/", create_media),
    path("delete/", delete_media),
    path("query_single/", query_single_media),
]
