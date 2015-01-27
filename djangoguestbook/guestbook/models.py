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
	def get_lastest(cls, guestbook_name, count=10, force_new=False):
		if(not force_new):
			greetings = memcache.get('%s:greetings' % guestbook_name)
			if greetings:
				return greetings
			else:
				greetings = cls._query_update_memcache(guestbook_name, count)
		else:
			greetings = cls._query_update_memcache(guestbook_name, count)
		return greetings

	@classmethod
	def _query_update_memcache(cls, guestbook_name, count):
		greetings_query = cls.query(ancestor=ndb.Key(Guestbook, guestbook_name)).order(
			-cls.date)
		greetings = greetings_query.fetch(count)
		if not memcache.set('%s:greetings' % guestbook_name, greetings, count):
			logging.error('Memcache set failed.')
		return greetings

	@classmethod
	def put_from_dict(cls, dict):
		greeting = Greeting(parent=Guestbook.get_key(dict['guestbook_name']))
		if dict['author']:
			greeting.author = dict['author']
		greeting.content = dict['content']
		greeting.put()


class Guestbook(ndb.Model):
	@classmethod
	def get_key(cls, guestbook_name=DEFAULT_GUESTBOOK_NAME):
		return ndb.Key(cls, guestbook_name)

