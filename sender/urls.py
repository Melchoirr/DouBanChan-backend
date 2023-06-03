from django.urls import path
from sender.views import *

urlpatterns = [
    path("activate/<int:u_id>", activate),
]
