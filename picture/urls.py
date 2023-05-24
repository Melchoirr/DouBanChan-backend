from django.urls import path
from picture.views import *

urlpatterns = [
    path("upload/", upload),
]
