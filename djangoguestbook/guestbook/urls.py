__author__ = 'fatatoopc'
from django.conf.urls import *
from guestbook.views import main_page, sign_post

urlpatterns = patterns('',
    (r'^sign/$', sign_post),
    (r'^$', main_page),
)