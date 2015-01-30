from django import forms


class DeleteForm(forms.Form):
	greeting_id = forms.IntegerField(initial=0)
	guestbook_name = forms.CharField()


class PostForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea, max_length=10)
	guestbook_name = forms.CharField(initial="default_guestbook")

