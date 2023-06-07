from django.urls import path
from report.views import *

urlpatterns = [
    path("report_post/", report_post),
    path("delete_message/", delete_message),
    path("query_single/", query_single_report),
]
