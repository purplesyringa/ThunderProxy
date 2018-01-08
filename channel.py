from user import User
import time

class Channel(object):
	def __init__(self, name):
		self.name = name
		self.online = []

	def get_key(self):
		return None

	def get_topic(self):
		return None

	def get_online(self):
		return self.online

	def get_user(self, nick):
		return User(nick)

	def get_mode(self):
		return "+cnt"

	def get_creation_time(self):
		return int(time.time())

	def connect(self, nick):
		self.online.append(nick)

	# Modes
	def set_banmask(self, banmask):
		raise NotImplementedError()
	def set_limit(self, user, limit):
		raise NotImplementedError()
	def set_speak(self, user, value):
		raise NotImplementedError()
	def set_moderator(self, user, value):
		raise NotImplementedError()
	def set_private(self, value):
		raise NotImplementedError()
	def set_secret(self, value):
		raise NotImplementedError()
	def set_invite(self, value):
		raise NotImplementedError()
	def set_topic_by_operator(self, value):
		raise NotImplementedError()
	def set_moderated(self, value):
		raise NotImplementedError()

	# Messages
	def send(self, from_, message):
		pass