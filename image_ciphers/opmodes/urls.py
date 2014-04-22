from django.conf.urls import patterns, include, url
from . import views as oviews

urlpatterns = patterns('',
    url(r'^$', oviews.modes_operation, name='opmodes'),
    url(r'^get_zip/(?P<temp_zip>.{0,12})/$', oviews.get_zip, name='opmodes-get_zip'),
    url(r'^get_img/(?P<temp_img>.{0,15})/$', oviews.get_img, name='opmodes-get_img'),
    url(r'^decrypt/$', oviews.modes_operation_decrypt, name='opmodes-decrypt'),
    url(r'^encrypt/$', oviews.modes_operation_encrypt, name='opmodes-encrypt'),
    url(r'^expansion/$', oviews.Expansion.as_view(), name='expansion'),
)
