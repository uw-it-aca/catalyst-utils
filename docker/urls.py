from .base_urls import *
from django.urls import include, re_path

urlpatterns += [
    re_path(r'^', include('catalyst_utils.urls')),
    re_path(r'^support/', include('userservice.urls')),
    re_path(r'^restclients/', include('rc_django.urls')),
]
