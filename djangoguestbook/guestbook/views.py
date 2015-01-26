import urllib
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from google.appengine.api import users
from google.appengine.api import memcache
from guestbook.models import Greeting, Guestbook, DEFAULT_GUESTBOOK_NAME


class GreetingView(TemplateView):
	template_name = "guestbook/main_page.html"
	
	def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greetings = Guestbook.get_greetings(guestbook_name)
		if users.get_current_user():
			url = users.create_logout_url(self.request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linktext = 'Login'
		template_values = {
			'greetings': greetings,
			'guestbook_name': guestbook_name,
			'url': url,
			'url_linktext': url_linktext,
		}
		context = template_values
		return context

	def post(self, request):
		if request.method == 'POST':
			guestbook_name = request.POST.get('guestbook_name')
			greeting = Greeting(parent=Guestbook.get_guestbook_key(guestbook_name))
			if users.get_current_user():
				greeting.author = users.get_current_user()
			greeting.content = request.POST.get('content')
			greeting.put()
			# update to memcache
			greetings = memcache.get('%s:greetings' % guestbook_name)
			greetings.insert(0, greeting)
			memcache.set('%s:greetings' % guestbook_name, greetings)
			context = HttpResponseRedirect(
				'/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
		else:
			context = HttpResponseRedirect('/')
		return context















