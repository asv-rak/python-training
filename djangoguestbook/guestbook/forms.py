from django import forms
from google.appengine.api import users
from guestbook.models import Greeting


class PostForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea, max_length=10)
	guestbook_name = forms.CharField(initial="default_guestbook")


class EditGreetingForm(forms.Form):
	guestbook_name = forms.CharField(
		widget=forms.HiddenInput(),
		required=False)
	greeting_id = forms.CharField(
		widget=forms.HiddenInput(),
		required=False,
	)
	greeting_author = forms.CharField(
		label="Author",
		required=False,
		widget=forms.TextInput(attrs={'readonly':'readonly'})
	)
	greeting_content = forms.CharField(
		label="",
		required=True,
		max_length=10,
		widget=forms.Textarea
	)

	def update_greeting(self):
		if users.get_current_user():
			greeting_updated_by = users.get_current_user().nickname()
		else:
			greeting_updated_by = None
		dict = {
			'greeting_id': self.cleaned_data['greeting_id'],
			'guestbook_name': self.cleaned_data['guestbook_name'],
			'update_by': greeting_updated_by,
			'content': self.cleaned_data['greeting_content'],
		}
		new_greeting = Greeting.update_from_dict(dict)
		return new_greeting


class APIEditGreetingForm(forms.Form):
	greeting_author = forms.CharField(
		label="Author",
		required=False,
		widget=forms.TextInput(attrs={'readonly': 'readonly'})
	)
	greeting_content = forms.CharField(
		label="",
		required=True,
		max_length=10,
		widget=forms.Textarea,
	)

	def update_greeting(self, guestbook_name, greeting_id):
		greeting_content = self.cleaned_data['greeting_content']
		if users.get_current_user():
			greeting_updated_by = users.get_current_user().nickname()
		else:
			greeting_updated_by = None
		dict = {
			'greeting_id': greeting_id,
			'guestbook_name': guestbook_name,
			'update_by': greeting_updated_by,
			'content': self.cleaned_data['greeting_content'],
		}
		new_greeting = Greeting.update_from_dict(dict)
		return new_greeting














