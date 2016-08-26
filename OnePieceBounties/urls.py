from django.conf.urls import include, url
from django.contrib import admin
from bounties import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'OnePieceBounties.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^onepiecebounties/', views.index, name='index'),
    # url(r'^admin/', include(admin.site.urls)),
]
