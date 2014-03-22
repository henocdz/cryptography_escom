from django.conf.urls import patterns, include, url
from django.contrib import admin
from opmodes import urls as opurls

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'image_ciphers.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'opmodes.views.home', name='project-home'),
    url(r'^modes-of-operation/', include(opurls.urlpatterns)),
    url(r'^admin/', include(admin.site.urls)),
)
