"""DouBanChan_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('user/', include('user.urls')),
    path('media/', include('media.urls')),
    path('group/', include('group.urls')),
    path('chat/', include('chat.urls')),
    path("base/", include('base.urls')),
    path("picture/", include('picture.urls')),
    path("text/", include('text.urls')),
    path("post/", include('post.urls')),
    path("report/", include('report.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
