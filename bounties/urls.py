from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pirate_id>\d+)/$', views.get_pirate, name='get_pirate'),
]
