from django import forms
from google.appengine.api import users
from guestbook.models import Greeting


class PostForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea, max_length=10)
	guestbook_name = forms.CharField(initial="default_guestbook")


class EditGreetingForm(forms.Form):
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
















