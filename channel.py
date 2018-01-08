from user import User

class Channel(object):
	def __init__(self, name, key=None):
		self.name = name
		self.key = key
		self.online = []

	def get_topic(self):
		return None

	def get_online(self):
		return self.online

	def get_user(self, nick):
		return User(nick)

	def connect(self, nick):
		self.online.append(nick)