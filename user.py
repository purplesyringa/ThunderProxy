class User(object):
	def __init__(self, nick, username, hostname):
		self.nick = nick
		self.username = username
		self.hostname = hostname

		self.is_away = False
		self.away_reason = None

	def set_away(self, is_away, reason=None):
		self.is_away = is_away
		self.away_reason = reason