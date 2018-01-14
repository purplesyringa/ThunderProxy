from irc.util import NickError
from thunderwave import Singleton as ThunderWave

class User(object):
	def __init__(self, nick, username, hostname, server):
		self.nick = nick
		self.username = username
		self.hostname = hostname
		self.is_away = False
		self.away_reason = None
		self.channels = []
		self.transactions = []

	def set_away(self, is_away, reason=None):
		self.is_away = is_away
		self.away_reason = reason

	def change_nick(self, new_nick):
		for chan in self.channels:
			try:
				chan.broadcast(self, "NICK %s" % new_nick)
			except Exception as e:
				continue

		self.nick = new_nick

	def join(self, chan):
		self.channels.append(chan)
	def part(self, chan):
		self.channels.remove(chan)

	def connect(self, transaction):
		self.transactions.append(transaction)
	def disconnect(self, transaction):
		self.transactions.remove(transaction)

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
	def send(self, user, message):
		pass

	def receivePrivMsg(self, user, message, chan=None):
		to = None
		if chan is None:
			to = self.nick
		else:
			to = chan.name

		self.broadcast(user, "PRIVMSG %s :%s" % (to, message))
	def broadcast(self, user, data):
		for transaction in self.transactions:
			transaction.sendall(":%s!%s@%s %s" % (user.nick, user.username, user.hostname, data))

	@staticmethod
	def check_nick(nick):
		return True