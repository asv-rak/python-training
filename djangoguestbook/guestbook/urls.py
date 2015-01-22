from django.conf.urls import patterns, url
from guestbook.views import GreetingView

urlpatterns = patterns('',
    url(r'^$', GreetingView.as_view(), name='home'),
    url(r'^sign/$', GreetingView.as_view(), name='sign'),
)