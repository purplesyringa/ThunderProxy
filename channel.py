from user import User
import time
from thunderwave import ThunderWave

class Channel(object):
	def __init__(self, name):
		self.name = name
		self.online = []
		self.tw = ThunderWave()
		self.broadcast = lambda nick, username, message: None

	def get_key(self):
		return None

	def get_topic(self):
		if self.name == "#lobby":
			return dict(topic="ThunderWave lobby", author="glightstar!glightstar@localhost", time=1491048465079)
		else:
			return dict(topic="", author="", time=0)

	def get_online(self):
		return self.online

	def get_user(self, nick):
		return User(nick)

	def get_mode(self):
		return "+cnt"

	def get_creation_time(self):
		return 1491048465079

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
	def send(self, nick, username, message):
		if self.name == "#lobby":
			address = None
			try:
				address = self.tw.from_cert_user_id(nick.replace("/", "@"))
			except KeyError:
				errmsg = """
					Hello, %s!
					Unfortunately, ThunderProxy could not find
					correct auth_address for your nickname.
					Make sure that your nick is set like
					gitcenter/zeroid.bit or glightstar/kaffie.bit.
					With regards, Ivanq.
				""".replace("\n", " ").replace("\t", "") % nick
				self.broadcast("ThunderProxy", "tp", errmsg)
				return

			self.tw.send_to_lobby(address=address, body=message)