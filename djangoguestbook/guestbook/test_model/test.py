from unittest import TestCase
from datetime import datetime
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from mock import patch
from guestbook.models import Greeting, Guestbook, DEFAULT_GUESTBOOK_NAME


class TestBaseClass(TestCase):
	guestbook_name = DEFAULT_GUESTBOOK_NAME

	def setUp(self):
		self.testbed = testbed.Testbed()
		# active for use
		self.testbed.activate()
		# declare some service for use
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		self.testbed.init_user_stub()
		# creat test
		for i in range(0, 20, 1):
			dict = {
				'guestbook_name': self.guestbook_name,
				'author': "test_author",
				'content': "testing"
			}
			Greeting.put_from_dict(dict)

	def tearDown(self):
		self.testbed.deactivate()


class TestGreeting(TestBaseClass):

	def test_get_lastest_with_correct_guestbook_name_non_cache(self):
		with patch('google.appengine.api.memcache.get') as func:
			val_return = None
			func.return_value = val_return
			greetings = Greeting.get_lastest(self.guestbook_name, 10, False)
			assert greetings is not None and len(greetings) == 10

	def test_get_lastest_with_correct_guestbook_name_have_cache(self):
		with patch('google.appengine.api.memcache.get') as func:
			val_return = Greeting._query_update_memcache(self.guestbook_name, 10)
			func.return_value = val_return
			greetings = Greeting.get_lastest(self.guestbook_name, 10, False)
			assert greetings is not None and len(greetings) == 10

	def test_get_lastest_with_wrong_guestbook_name_non_cache(self):
		with patch('google.appengine.api.memcache.get') as func:
			val_return = None
			func.return_value = val_return
			greetings = Greeting.get_lastest("wrong_guestbook", 10, False)
			assert greetings is not None and len(greetings) == 0

	def test_get_lastest_with_wrong_guestbook_name_have_cache(self):
		with patch('google.appengine.api.memcache.get') as func:
			val_return = Greeting._query_update_memcache(self.guestbook_name, 10)
			func.return_value = val_return
			greetings = Greeting.get_lastest("wrong_guestbook", 10, False)
			assert greetings is not None and len(greetings) == 0

	def test_get_lastest_with_out_of_size_non_cache(self):
		with patch('google.appengine.api.memcache.get') as func:
			val_return = None
			func.return_value = val_return
			greetings = Greeting.get_lastest(self.guestbook_name, 30, False)
			assert greetings is not None and len(greetings) == 20

	def test_get_lastest_with_out_of_size_have_cache(self):
		with patch('google.appengine.api.memcache.get') as func:
			val_return = Greeting._query_update_memcache(self.guestbook_name, 30)
			func.return_value = val_return
			greetings = Greeting.get_lastest(self.guestbook_name, 30, False)
			assert greetings is not None and len(greetings) == 20

	def test_get_lastest_with_in_of_size_non_cache(self):
		with patch('google.appengine.api.memcache.get') as func:
			val_return = None
			func.return_value = val_return
			greetings = Greeting.get_lastest(self.guestbook_name, 5, False)
			assert greetings is not None and len(greetings) == 5

	def test_get_lastest_with_in_of_size_have_cache(self):
		with patch('google.appengine.api.memcache.get') as func:
			val_return = Greeting._query_update_memcache(self.guestbook_name, 5)
			func.return_value = val_return
			greetings = Greeting.get_lastest(self.guestbook_name, 5, False)
			assert greetings is not None and len(greetings) == 5

	def test__query_update_memcache(self):
		greetings = Greeting._query_update_memcache(self.guestbook_name, 10)
		assert greetings is not None and len(greetings) == 10

	def test_put_from_dict(self):
		dict = {
			'guestbook_name': self.guestbook_name,
			'author': "test_author",
			'content': "testing"
		}
		greeting = Greeting.put_from_dict(dict)
		assert \
			greeting is not None and \
			greeting.author == "test_author" and \
			greeting.content == "testing"

	def test_update_from_dict_with_right_id(self):
		dict = {
			'guestbook_name': self.guestbook_name,
			'author': "test_author",
			'content': "testing"
		}
		greeting = Greeting.put_from_dict(dict)
		updated_dict = {
			'guestbook_name': self.guestbook_name,
			'greeting_id': greeting.key.id(),
			'update_by': "updated_author",
			'content': "updated"
		}
		updated_greeting = Greeting.update_from_dict(updated_dict)
		assert \
			updated_greeting is not None and \
			updated_greeting.author == "test_author" and \
			updated_greeting.content == "updated" and \
			updated_greeting.updated_by == "updated_author"

	def test_update_from_dict_with_wrong_id(self):
		dict = {
			'guestbook_name': self.guestbook_name,
			'author': "test_author",
			'content': "testing"
		}
		greeting = Greeting.put_from_dict(dict)
		updated_dict = {
			'guestbook_name': self.guestbook_name,
			'greeting_id': greeting.key.id()+1,
			'update_by': "updated_author",
			'content': "updated"
		}
		updated_greeting = Greeting.update_from_dict(updated_dict)
		assert \
			updated_greeting is None

	def test_get_greeting_with_right_id(self):
		dict = {
			'guestbook_name': self.guestbook_name,
			'author': "test_author",
			'content': "testing"
		}
		greeting = Greeting.put_from_dict(dict)
		got_greeting = Greeting.get_greeting_by_id(self.guestbook_name, greeting.key.id())
		assert got_greeting is not None and got_greeting == greeting

	def test_get_greeting_with_wrong_id(self):
		got_greeting = Greeting.get_greeting_by_id(self.guestbook_name, 999)
		assert got_greeting is None

	def test_delete_greeting_wiht_right_id(self):
		dict = {
			'guestbook_name': self.guestbook_name,
			'author': "test_author",
			'content': "testing"
		}
		greeting = Greeting.put_from_dict(dict)
		Greeting.delete_greeting_by_id(self.guestbook_name, greeting.key.id())
		got_greeting = Greeting.get_greeting_by_id(self.guestbook_name, greeting.key.id())
		assert got_greeting is None

	def test_delete_greeting_wiht_wrong_id(self):
		dict = {
			'guestbook_name': self.guestbook_name,
			'author': "test_author",
			'content': "testing"
		}
		greeting = Greeting.put_from_dict(dict)
		Greeting.delete_greeting_by_id(self.guestbook_name, greeting.key.id()+1)
		got_greeting = Greeting.get_greeting_by_id(self.guestbook_name, greeting.key.id())
		assert got_greeting is not None and got_greeting == greeting

	def test_to_dict_with_right_data(self):
		greeting = Greeting()
		greeting.author = "test_author"
		greeting.content = "testing"
		greeting.date = datetime.strptime('2015-02-11 13:00 +0000', "%Y-%m-%d %H:%M +0000")
		greeting.updated_by = "updated_author"
		greeting.updated_date = datetime.strptime('2015-02-11 13:00 +0000', "%Y-%m-%d %H:%M +0000")
		greeting.put()
		dict = greeting.to_dict()
		assert dict['id'] == greeting.key.id() and\
			dict['author'] == "test_author" and\
			dict['content'] == "testing" and\
			dict['date'] == "2015-02-11 13:00 +0000" and\
			dict['updated_by'] == "updated_author" and\
			dict['updated_date'] == "2015-02-11 13:00 +0000"

	def test_to_dict_with_wrong_id(self):
		greeting = Greeting()
		greeting.author = "test_author"
		greeting.content = "testing"
		greeting.date = datetime.strptime('2015-02-11 13:00 +0000', "%Y-%m-%d %H:%M +0000")
		greeting.updated_by = "updated_author"
		greeting.updated_date = datetime.strptime('2015-02-11 13:00 +0000', "%Y-%m-%d %H:%M +0000")
		greeting.put()
		dict = greeting.to_dict()
		assert dict['id'] != greeting.key.id() + 1

	def test_to_dict_with_wrong_some_data(self):
		greeting = Greeting()
		greeting.author = "test_author"
		greeting.content = "testing"
		greeting.date = datetime.strptime('2015-02-11 13:00 +0000', "%Y-%m-%d %H:%M +0000")
		greeting.updated_by = "updated_author"
		greeting.updated_date = datetime.strptime('2015-02-11 13:00 +0000', "%Y-%m-%d %H:%M +0000")
		greeting.put()
		dict = greeting.to_dict()
		assert dict != "update_author"

	def test_get_greeting_with_no_cursor_in_of_size(self):
		total_count = len(Greeting.query(ancestor=ndb.Key(Guestbook, self.guestbook_name)).order(
			-Greeting.date).fetch())
		num_greetings = 10
		greetings, next_cursor, more = Greeting.get_greeting(self.guestbook_name, num_greetings, None)
		assert \
			greetings is not None and\
			next_cursor is not None and \
			more is (num_greetings < total_count)

	def test_get_greeting_with_no_cursor_out_of_size(self):
		total_count = len(Greeting.query(ancestor=ndb.Key(Guestbook, self.guestbook_name)).order(
			-Greeting.date).fetch())
		num_greetings = 21
		greetings, next_cursor, more = Greeting.get_greeting(self.guestbook_name, num_greetings, None)
		assert \
			greetings is not None and\
			next_cursor is not None and\
			more is (num_greetings < total_count)

	def test_get_greeting_with_right_cursor_in_of_size(self):
		total_count = len(Greeting.query(ancestor=ndb.Key(Guestbook, self.guestbook_name)).order(
			-Greeting.date).fetch())
		num_greetings = 10
		greetings_tmp, nextcurs_tmp, more_tmp = Greeting.get_greeting(self.guestbook_name, 1, None)
		greetings, next_cursor, more = Greeting.get_greeting(
			self.guestbook_name,
			num_greetings,
			nextcurs_tmp.urlsafe())
		assert \
			greetings is not None and \
			next_cursor is not None and \
			more is (num_greetings < total_count)

	def test_get_greeting_with_right_cursor_out_of_size(self):
		total_count = len(Greeting.query(ancestor=ndb.Key(Guestbook, self.guestbook_name)).order(
			-Greeting.date).fetch())
		num_greetings = 21
		greetings_tmp, nextcurs_tmp, more_tmp = Greeting.get_greeting(self.guestbook_name, 1, None)
		greetings, next_cursor, more = Greeting.get_greeting(
			self.guestbook_name,
			num_greetings,
			nextcurs_tmp.urlsafe())
		assert \
			greetings is not None and \
			next_cursor is not None and \
			more is (num_greetings < total_count)

	def test_get_greeting_with_wrong_cursor(self):
		greetings, next_cursor, more = Greeting.get_greeting(self.guestbook_name, 21, "worng cursor")
		assert greetings is None and next_cursor is None


class TestGuestbook(TestBaseClass):
	def test_get_key_with_right_guestbook_name(self):
		x = ndb.Key(Guestbook, self.guestbook_name)
		assert x == Guestbook.get_key(self.guestbook_name)

	def test_get_key_with_wrong_guestbook_name(self):
		x = ndb.Key(Guestbook, "wrong guestbook_name")
		assert x != Guestbook.get_key(self.guestbook_name)