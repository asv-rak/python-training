from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns(
	'',
	(r'^', include('guestbook.urls')),
)
