from django.views.generic.base import TemplateView
from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME
from google.appengine.api import users
from django.http import HttpResponseRedirect
import urllib

class GreetingView(TemplateView):
    template_name = "guestbookcbv/main_page.html"
    def get(self, request, *args, **kwargs):
        guestbook_name = request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)
        if users.get_current_user():
            url = users.create_logout_url(request.get_full_path())
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(request.get_full_path())
            url_linktext = 'Login'
        template_values = {
            'greetings': greetings,
            'guestbook_name': guestbook_name,
            'url': url,
            'url_linktext': url_linktext,
        }
        context = template_values
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            guestbook_name = request.POST.get('guestbook_name')
            greeting = Greeting(parent=guestbook_key(guestbook_name))
            if users.get_current_user():
                greeting.author = users.get_current_user()
            greeting.content = request.POST.get('content')
            greeting.put()
            context = HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
        else: context = HttpResponseRedirect('/')
        return context

