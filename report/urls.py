from django.urls import path
from report.views import *

urlpatterns = [
    path("delete_message/", delete_message),
    path("query_single/", query_single_report),
    path("query_report/", query_report),
    path("report_post/", report_post),
    path("report_text/", report_text)
]
