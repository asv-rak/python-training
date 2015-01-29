from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib import admin

urlpatterns = patterns(
	'',
	(r'^', include('guestbook.urls')),
	(r'^admin/', include(admin.site.urls))
)
