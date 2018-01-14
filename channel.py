from user import User
import time
from thunderwave import Singleton as ThunderWave

class Channel(object):
	def __init__(self, name, server):
		self.name = name
		self.online = []
		self.tw = ThunderWave()
		self.tp_user = server.register_user(nick="ThunderProxy", username="tp", hostname="tp", transaction=None)

	def get_key(self):
		return None

	def get_topic(self):
		if self.name == "#lobby":
			return dict(topic="ThunderWave lobby", author="glightstar!glightstar@localhost", time=1491048465079)
		else:
			return dict(topic="", author="", time=0)

	def get_online(self):
		return self.online

	def get_mode(self):
		return "+cnt"

	def get_creation_time(self):
		return 1491048465079

	def connect(self, user):
		self.online.append(user)
	def disconnect(self, user):
		try:
			self.online.remove(user)
		except ValueError:
			pass

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

	def receiveMsg(self, user, message):
		for to in self.online:
			to.receivePrivMsg(user, message, chan=self)
	def broadcast(self, data):
		for to in self.online:
			to.broadcast(data)

	# Messages
	def send(self, user, message):
		if self.name == "#lobby":
			address = None
			try:
				address = self.tw.from_cert_user_id(user.nick.replace("/", "@"))
			except KeyError:
				errmsg = """
					Hello, %s!
					Unfortunately, ThunderProxy could not find
					correct auth_address for your nickname.
					Make sure that your nick is set like
					gitcenter/zeroid.bit or glightstar/kaffie.bit.
					With regards, Ivanq.
				""".replace("\n", " ").replace("\t", "") % user.nick
				self.receiveMsg(self.tp_user, errmsg)
				return

			self.tw.send_to_lobby(address=address, body=message)