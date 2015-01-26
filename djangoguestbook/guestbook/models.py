import logging
from google.appengine.ext import ndb
from google.appengine.api import memcache

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.


class Greeting(ndb.Model):
	'''Models an individual Guestbook entry.'''
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def creat_greeting(cls, guestbook_name):
		return Greeting(parent=Greeting.get_lastest(guestbook_name))

	@classmethod
	def get_lastest(cls, guestbook_name=DEFAULT_GUESTBOOK_NAME):
		return ndb.Key('Guestbook', guestbook_name)


class Guestbook():
	@classmethod
	def get_greetings(cls, guestbook_name):
		greetings = memcache.get('%s:greetings' % guestbook_name)
		if greetings is not None:
			return greetings
		else:
			greetings_query = Greeting.query(
				ancestor=Greeting.get_lastest(guestbook_name)).order(
				-Greeting.date)
			greetings = greetings_query.fetch(10)
			if not memcache.add('%s:greetings' % guestbook_name, greetings, 10):
				logging.error('Memcache set failed.')
		return greetings