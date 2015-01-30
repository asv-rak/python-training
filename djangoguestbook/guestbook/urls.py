from django.conf.urls import patterns, url
from guestbook.views import GreetingView, DeleteGreetingView

urlpatterns = patterns(
	'',
	url(r'^$', GreetingView.as_view(), name='home'),
	url(r'^sign/$', GreetingView.as_view(), name='sign'),
	url(r'^delete/$', DeleteGreetingView.as_view(), name='delete'),
)