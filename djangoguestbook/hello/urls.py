__author__ = 'fatatoopc'
from django.conf.urls import *
from hello.views import current
urlpatterns = patterns('',
    (r'^$', current),
)
