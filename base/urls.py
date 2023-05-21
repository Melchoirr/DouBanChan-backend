from django.urls import path
from base.views import *

urlpatterns = [
    path("query_base/", query_base),
    path("query_user/", query_user),
    path("query_chat/", query_chat),
    path("query_group/", query_group),
    path("query_media/", query_media),
    path("query_report/", query_report),
]
