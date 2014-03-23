from django.conf.urls import patterns, include, url
from . import views as oviews

urlpatterns = patterns('',
    url(r'^$', oviews.modes_operation, name='opmodes'),
    url(r'^get_zip/(?P<temp_zip>.{0,12})/$', oviews.get_zip, name='opmodes-decrypt'),
    url(r'^decrypt/$', oviews.modes_operation_decrypt, name='opmodes-decrypt'),
    url(r'^encrypt/$', oviews.modes_operation_encrypt, name='opmodes-encrypt'),
)
