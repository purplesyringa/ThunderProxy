from irc.util import NickError
from thunderwave import Singleton as ThunderWave

class User(object):
	def __init__(self, nick):
		self.nick = nick
		self.is_away = False
		self.away_reason = None

	def set_away(self, is_away, reason=None):
		self.is_away = is_away
		self.away_reason = reason

	def is_admin(self):
		return False
	def is_moderator(self):
		return False

	# Modes
	def set_invisible(self, value):
		raise NotImplementedError()
	def set_receipt_server_notices(self, value):
		raise NotImplementedError()
	def set_wallops(self, value):
		raise NotImplementedError()
	def set_moderator(self, value):
		raise NotImplementedError()

	# Messages
	def send(self, nick, username, message):
		pass

	@staticmethod
	def check_nick(nick):
		return True