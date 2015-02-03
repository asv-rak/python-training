from django import forms


class PostForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea, max_length=10)
	guestbook_name = forms.CharField(initial="default_guestbook")


class EditForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea, max_length=10)
	greeting_id = forms.IntegerField()
	guestbook_name = forms.CharField()

