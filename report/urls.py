from django.urls import path
from report.views import *

urlpatterns = [
    path("add_report/", add_report),
    # path("delete_report/", delete_report),
    path("query_single/", query_single_report),
]
