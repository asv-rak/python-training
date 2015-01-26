__author__ = 'fatatoopc'
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import logging
import urllib
import webapp2
JINJA2_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


def guestbook_key(guestbook_name = DEFAULT_GUESTBOOK_NAME):
	return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date  = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
	def get(self):
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greetings = self.get_greetings(guestbook_name)
		stats = memcache.get_stats()
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		template_values = {
			'greetings': greetings,
			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
			'statshits': stats['hits'],
			'statsmisses': stats['misses'],
		}
		template = JINJA2_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

	def get_greetings(self, guestbook_name):
		greetings = memcache.get('%s:greetings' % guestbook_name)
		if greetings is not None:
			return greetings
		else:
			greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
			greetings = greetings_query.fetch(10)
			if not memcache.set('%s:greetings' % guestbook_name, greetings, 10):
				logging.error('Memcache set failed.')
		return greetings


class Guestbook(webapp2.RequestHandler):
	def post(self):
		logging.warning("Go first!!!!!")
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greeting = Greeting(parent=guestbook_key(guestbook_name))
		if users.get_current_user():
			greeting.author = users.get_current_user()
		greeting.content = self.request.get('content')
		greeting.put()
		# update to memcache
		greetings = memcache.get('%s:greetings' % guestbook_name)
		greetings.insert(0,greeting)
		memcache.set('%s:greetings' % guestbook_name, greetings)
		# redirect
		query_params = {'guestbook_name': guestbook_name}
		self.redirect('/?' + urllib.urlencode(query_params))

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/sign', Guestbook)
], debug=True)