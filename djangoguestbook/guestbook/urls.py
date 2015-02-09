from django.conf.urls import patterns, url
from guestbook.views import GreetingView
from guestbook.api import APIGreeting, APIDetailGreeting
urlpatterns = patterns(
	'',
	url(r'^$', GreetingView.as_view(), name='home'),
	url(r'^sign/$', GreetingView.as_view(), name='sign'),
	# API url handle
	url(
		r'^api/guestbook/(?P<guestbook_name>(.)+)/greeting/$',
		APIGreeting.as_view(),
		name="list-greeting"),
	url(
		r'^api/guestbook/(?P<guestbook_name>(.)+)/greeting/(?P<greeting_id>(.)+)$',
		APIDetailGreeting.as_view(),
		name="detail-greeting"),
)