from django.conf.urls import patterns, url
from guestbook.views import GreetingView, EditGreetingView

urlpatterns = patterns(
	'',
	url(r'^$', GreetingView.as_view(), name='home'),
	url(r'^sign/$', GreetingView.as_view(), name='sign'),
	url(r'^edit/$', GreetingView.as_view(), name='edit'),
	url(r'^edited/$', EditGreetingView.as_view(), name='edited'),
)