from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from bounties import urls as bounties_urls

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^onepiecebounties/', include(bounties_urls, namespace='bounties')),
    url(r'^admin/', include(admin.site.urls)),
] 
