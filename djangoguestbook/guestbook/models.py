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
		return Greeting(parent=Greeting.get_guestbook_key(guestbook_name))

	@classmethod
	def get_guestbook_key(cls, guestbook_name=DEFAULT_GUESTBOOK_NAME):
		return ndb.Key(cls, guestbook_name)

	@classmethod
	def get_lastest(cls, guestbook_name, count=10, force_new=False):
		if(not force_new):
			greetings = memcache.get('%s:greetings' % guestbook_name)
			if greetings is not None:
				return greetings
			else:
				cls.prefix_query_update_memcache(guestbook_name, count)
		else:
			cls.prefix_query_update_memcache(guestbook_name, count)
		return greetings

	@classmethod
	def prefix_query_update_memcache(self, guestbook_name, count):
		greetings_query = Greeting.query(ancestor=ndb.Key(Greeting, guestbook_name)).order(
			-Greeting.date)
		greetings = greetings_query.fetch(count)
		if not memcache.set('%s:greetings' % guestbook_name, greetings, count):
			logging.error('Memcache set failed.')


