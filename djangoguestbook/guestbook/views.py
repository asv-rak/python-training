import urllib
from django.views.generic.edit import FormView, HttpResponseRedirect
from guestbook.models import Greeting, DEFAULT_GUESTBOOK_NAME
from guestbook.forms import PostForm, DeleteForm
from google.appengine.api import users
from django import forms


class DeleteGreetingView(FormView):
	template_name = "guestbook/main_page.html"
	form_class = DeleteForm

	def form_valid(self, form):
		greeting_id = form.cleaned_data.get('greeting_id')
		guestbook_name = form.cleaned_data.get('guestbook_name')
		Greeting.delete_greeting(guestbook_name, int(greeting_id))
		return HttpResponseRedirect('/')


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
		if users.is_current_user_admin():
			admin = True
		else:
			admin = False
		template_values = {
			'greetings': greetings,
			'guestbook_name': guestbook_name,
			'url': url,
			'url_linktext': url_linktext,
			'form': kwargs['form'],
			'is_admin': admin
		}
		context = template_values
		return context

	@classmethod
	def set_force_new(cls, _force_new):
		cls.force_new = _force_new




