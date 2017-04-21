from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update_user_scan', views.update_scan_view),
    url(r'^compare', views.compare),
    url(r'^user_profile', views.get_user_profile),
    url(r'^user_scans', views.get_user_scans),
    url(r'^update_all_scans', views.update_all_scans),
]
