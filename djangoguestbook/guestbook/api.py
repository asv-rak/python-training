import json
from django.http import HttpResponse
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeletionMixin
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.api import users
from guestbook.forms import PostForm, EditGreetingForm
from guestbook.models import DEFAULT_GUESTBOOK_NAME, Greeting


class JSONResponseMixin(object):
	def render_to_response(self, context, **response_kwargs):
		return self.get_json_response(self.convert_context_to_json(context), **response_kwargs)

	def get_json_response(self, content, **httpresponse_kwargs):
		return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

	def convert_context_to_json(self, context):
		return json.dumps(context)


class APIGreeting(JSONResponseMixin, FormView):
	form_class = PostForm
	success_url = '/'

	def get(self, request, *args, **kwargs):
		try:
			Cursor(urlsafe=self.request.GET.get('cursor'))
		except:
			return HttpResponse(status=404)
		return super(APIGreeting, self).get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		request.POST = json.loads(request.body)
		return super(APIGreeting, self).post(self, request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		guestbook_name = self.kwargs.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		str_cursor = self.request.GET.get('cursor', None)
		greetings, next_cursor, next = Greeting.get_greeting(guestbook_name, 20, str_cursor)
		greetings_dict = [greeting.to_dict() for greeting in greetings]
		data = {}
		data['greeting'] = greetings_dict
		if next_cursor:
			data['cursor'] = next_cursor.urlsafe()
		data['next'] = next
		return data

	def form_valid(self, form):
		guestbook_name = form.cleaned_data.get('guestbook_name')
		dict = {
			'guestbook_name': guestbook_name,
			'author': users.get_current_user(),
			'content': form.cleaned_data.get('content')
		}
		new_greeting = Greeting.put_from_dict(dict)
		if new_greeting:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def form_invalid(self, form):
		return HttpResponse(status=400)


class APIDetailGreeting(JSONResponseMixin, DetailView, FormView, DeletionMixin):
	object = Greeting
	form_class = EditGreetingForm
	success_url = "/"

	def get_object(self, queryset=None):
		guestbook_name = self.kwargs.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greeting_id = self.kwargs.get('greeting_id', -1)
		greeting = Greeting.get_greeting_by_id(guestbook_name, greeting_id)
		if greeting:
			return greeting
		else:
			return None

	def get_context_data(self, **kwargs):
		if self.object:
			return self.object.to_dict()
		else:
			return HttpResponse(status=404)

	def put(self, request, *args, **kwargs):
		request.POST = json.loads(request.body)
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		greeting_id = self.kwargs.get('greeting_id', -1)
		guestbook_name = self.kwargs.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		if users.get_current_user():
			greeting_updated_by = users.get_current_user().nickname()
		else:
			greeting_updated_by = None
		dict = {
			'greeting_id': greeting_id,
			'guestbook_name': guestbook_name,
			'update_by': greeting_updated_by,
			'content': form.cleaned_data['greeting_content'],
		}
		new_greeting = Greeting.update_from_dict(dict)
		if new_greeting:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def form_invalid(self, form):
		return HttpResponse(status=400)

	def delete(self, request, *args, **kwargs):
		greeting_id = self.kwargs.get('greeting_id', -1)
		guestbook_name = self.kwargs.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		if Greeting.delete_greeting_by_id(guestbook_name, greeting_id):
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)