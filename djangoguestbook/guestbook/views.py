from django.http import HttpResponseRedirect
from django.shortcuts import render
from google.appengine.api import users
from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME
from google.appengine.api import memcache
import urllib
import logging

def main_page(request):
    guestbook_name = request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
    greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    greetings = get_greetings(guestbook_name)
    stats = memcache.get_stats()
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
        'statshits': stats['hits'],
        'statsmisses': stats['misses'],
    }
    return render(request, 'guestbook/main_page.html', template_values)

def sign_post(request):
    if request.method == 'POST':
        guestbook_name = request.POST.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = users.get_current_user()
        greeting.content = request.POST.get('content')
        greeting.put()
        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
    return HttpResponseRedirect('/')

def get_greetings(guestbook_name):
    greetings = memcache.get('%s:greetings' % guestbook_name)
    if greetings is not None:
        return greetings
    else:
        greetings = render_greetings(guestbook_name)
        if not memcache.add('%s:greetings' % guestbook_name, greetings, 10):
            logging.error('Memcache set failed.')
    return greetings

def render_greetings(guestbook_name):
    greetings_query = Greeting.query(
        ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    greetings = greetings_query.fetch(10)
    return greetings