import urllib
from django import forms
from django.views.generic.edit import FormView
from google.appengine.api import users
from guestbook.models import Greeting, DEFAULT_GUESTBOOK_NAME
from guestbook.forms import PostForm, EditForm


class EditGreetingView(FormView):
	template_name = "guestbook/edit_page.html"
	form_class = EditForm

	def form_valid(self, form):
		guestbook_name = form.cleaned_data.get('guestbook_name')
		dict = {
			'greeting_id': form.cleaned_data.get('greeting_id'),
			'guestbook_name': guestbook_name,
			'update_by': users.get_current_user(),
			'content': form.cleaned_data.get('content'),
		}
		Greeting.update_from_dict(dict)
		self.success_url = '/?' + urllib.urlencode({'guestbook_name': guestbook_name})
		return super(EditGreetingView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		greeting_id = long(self.request.GET.get('greeting_id', 0))
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		kwargs['form'] = EditForm(initial={'guestbook_name': guestbook_name, 'greeting_id': greeting_id})
		kwargs['form'].fields['greeting_id'].widget = forms.HiddenInput()
		template_values = {
			'form': kwargs['form'],
		}
		context = template_values
		return context


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

	def form_invalid(self, form):
		return super(GreetingView, self).form_invalid(form)

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
		user = users.get_current_user()
		template_values = {
			'greetings': greetings,
			'guestbook_name': guestbook_name,
			'url': url,
			'url_linktext': url_linktext,
			'form': kwargs['form'],
			'is_admin': admin,
			'current_user': user,
		}
		context = template_values
		return context

	@classmethod
	def set_force_new(cls, _force_new):
		cls.force_new = _force_new














