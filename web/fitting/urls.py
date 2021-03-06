from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update_user_scan', views.update_scan_view),
    url(r'^best_style', views.best_style),
    url(r'^best_size', views.best_size),
    url(r'^best_scan', views.best_scan),
    url(r'^user_profile', views.get_user_profile),
    url(r'^user_scans', views.get_user_scans),
    url(r'^update_all_scans', views.update_all_scans),
    url(r'^update_lasts', views.update_lasts_view),
    url(r'^set_default_scan', views.set_default_scan_view),
    url(r'^set_default_size', views.set_default_size_view),
    url(r'^generate_images', views.generate_images),
    url(r'^copy_last/(?P<pk>[0-9]+)/$', views.copy_last, name='copy_last',),
    url(r'^create_user', views.create_user),
    url(r'^generate_comparison_config', views.generate_comparison_config),
]
