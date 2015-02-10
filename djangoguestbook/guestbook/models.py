import logging
import datetime
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.datastore.datastore_query import Cursor

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.


class Greeting(ndb.Model):
	'''Models an individual Guestbook entry.'''
	author = ndb.StringProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
	updated_by = ndb.StringProperty()
	updated_date = ndb.DateTimeProperty(auto_now_add=True)

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
			greeting.author = dict['author'].nickname()
		else:
			greeting.author = None
		greeting.content = dict['content']
		greeting.put()
		return greeting

	@classmethod
	def update_from_dict(cls, dict):
		greeting = cls.get_greeting_by_id(dict['guestbook_name'], dict['greeting_id'])
		if greeting:
			greeting.content = dict['content']
			greeting.update_by = dict['update_by']
			greeting.update_date = datetime.datetime.now()
			greeting.put()
			cls._query_update_memcache(dict['guestbook_name'], 10)
		return greeting

	@classmethod
	def get_greeting_by_id(cls, guestbook_name, greeting_id):
		key = ndb.Key(Guestbook, guestbook_name, cls, int(greeting_id))
		greeting = key.get()
		return greeting

	@classmethod
	def delete_greeting_by_id(cls,guestbook_name, greeting_id):
		try:
			id = int(greeting_id)
		except ValueError:
			return False
		if int(id) > 0:
			key = ndb.Key(Guestbook, guestbook_name, cls, int(greeting_id))
			if key:
				greeting = key.get()
				if greeting:
					key.delete()
					memcache.delete('%s:greetings' % guestbook_name)
					return True
		return False

	def to_dict(self, include=None, exclude=None):
		dict = {
			"id": self.key.id(),
			"content": self.content,
			"date": self.date.strftime("%Y-%m-%d %H:%M +0000"),
			"updated_by": self.updated_by
		}
		if self.author:
			dict['author'] = self.author
		else:
			dict['author'] = "Anonymous"

		if self.updated_date:
			dict['updated_date'] = self.updated_date.strftime("%Y-%m-%d %H:%M +0000")
		else:
			dict['updated_date'] = None

		return dict

	@classmethod
	def get_greeting(cls, guestbook_name=DEFAULT_GUESTBOOK_NAME, num_greetings=20, str_cursor=None):
		if num_greetings <= 0:
			greetings = None
			next_cursor = None
			more = None
		try:
			guestbook_key = Guestbook.get_key(guestbook_name)
			cursor = Cursor(urlsafe=str_cursor)
			greetings, next_cursor, more = cls.query(ancestor=guestbook_key).order(-Greeting.date)\
				.fetch_page(num_greetings, start_cursor=cursor)
		except:
			greetings = None
			next_cursor = None
			more = None
		return greetings, next_cursor, more


class Guestbook(ndb.Model):
	@classmethod
	def get_key(cls, guestbook_name=DEFAULT_GUESTBOOK_NAME):
		return ndb.Key(cls, guestbook_name)
