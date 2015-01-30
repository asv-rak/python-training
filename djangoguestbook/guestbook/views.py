import urllib
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from google.appengine.api import users
from google.appengine.api.mail import send_mail
try:
	from google.appengine.api.labs import taskqueue
except:
	from google.appengine.api import taskqueue
from google.appengine.ext import ndb
from guestbook.models import Greeting, DEFAULT_GUESTBOOK_NAME
from guestbook.forms import PostForm


class GreetingView(FormView):
	template_name = "guestbook/main_page.html"
	force_new = False
	form_class = PostForm

	def form_valid(self, form):
		guestbook_name = form.cleaned_data.get('guestbook_name')
		dict = {
			'guestbook_name': guestbook_name,
			'author': users.get_current_user(),
			'content': form.cleaned_data.get('content')
		}
		Greeting.put_from_dict(dict)
		self.success_url = '/?' + urllib.urlencode({'guestbook_name': guestbook_name})
		self.__class__.set_force_new(True)
		taskqueue.add(
			url='/mail',
			method='GET',
			params={
				'subject': dict['guestbook_name'],
				'body': dict['content'],
				'sender': dict['author'],
				'receiver': 'phamtangtung@gmail.com',
				}
		)
		return super(GreetingView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greetings = Greeting.get_lastest(guestbook_name, 10, self.force_new)
		self.__class__.set_force_new(False)
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
			'form': kwargs['form']
		}
		context = template_values
		return context

	@classmethod
	def set_force_new(cls, _force_new):
		cls.force_new = _force_new


class MailView(TemplateView):

	@ndb.transactional
	def get(self, request, *args, **kwargs):
		send_mail(
			self.request.GET.get('sender'),
			self.request.GET.get('receiver'),
			self.request.GET.get('subject'),
			self.request.GET.get('body')
		)
		return HttpResponse("Done")








