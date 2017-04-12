from django.conf.urls import url, include
from django.contrib import admin

from api.brands import *
from api.user import *

urlpatterns = [
    url(r'', include('api.urls', namespace='api')),
    url(r'^admin/', admin.site.urls),
    url(r'^fitting/', include('fitting.urls')),
]
