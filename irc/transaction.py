from util import debug, critical, ServerError, CommandError
from util import replycodes, errorcodes
import re

class Transaction(object):
	def __init__(self, nick, username, hostname, Channel, User, conn):
		self.nick = nick
		self.username = username
		self.hostname = hostname
		self.channels = []
		self.Channel = Channel
		self.user = User(nick)
		self.conn = conn
		self.init()

	def sendall(self, *args, **kwargs):
		return self.conn.sendall(*args, **kwargs)
	def recvall(self, *args, **kwargs):
		return self.conn.recvall(*args, **kwargs)

	def reply(self, code, data):
		self.sendall(":localhost %s %s %s" % (code, self.nick, data))
	def error(self, code, data):
		self.reply(errorcodes[code][0], "%s %s" % (errorcodes[code][1], data))
	def ok(self, code, data):
		self.reply(replycodes[code], data)

	def init(self):
		self.ok(
			"RPL_WELCOME",
			":Welcome to the Internet Relay Network %s!%s@%s" % (self.nick, self.username, self.hostname)
		)

	def commandJoin(self, channels, keys=None):
		channels = channels.split(",")
		keys = keys.split(",") if keys is not None else []

		channels = map(None, channels, keys) # This is like zip() but with padding

		for channel in channels:
			chan = self.get_channel(channel[0])
			if chan.get_key() != channel[1]:
				self.error("ERR_BADCHANNELKEY", "")
				return

			chan.connect(self.nick)

			# Specify online users
			online = chan.get_online()
			online = [(nick, chan.get_user(nick)) for nick in online]
			online = [
				"@" + user[0] if user[1].is_admin() else
				"+" + user[0] if user[1].is_moderator() else
				user[0]

				for user in online
			]
			online = " ".join(online)

			self.ok("RPL_NAMREPLY", "@ %s :%s" % (channel[0], online))
			self.ok("RPL_ENDOFNAMES", "%s :End of /NAMES list." % channel[0])

	def get_channel(self, channel):
		chan = self.Channel(channel)
		self.channels.append(chan)
		return chan

	def commandAway(self, reason=None):
		if reason is None:
			self.user.set_away(False)
			self.ok("RPL_UNAWAY", "")
		else:
			self.user.set_away(True, reason=reason)
			self.ok("RPL_NOWAWAY", "")

	def commandMode(self, nick, *args):
		if nick[0] in "#&":
			# Channel
			channel = nick
			chan = self.get_channel(channel)

			if len(args) == 0:
				# Send mode
				self.ok("RPL_CHANNELMODEIS", "%s %s" % (channel, chan.get_mode()))
				self.ok("RPL_CREATIONTIME", "%s %s" % (channel, chan.get_creation_time()))
				return
		else:
			# User
			if nick != self.nick:
				self.error("ERR_USERSDONTMATCH", "")
				return

			if len(args) == 0:
				# Send mode
				self.ok("RPL_UMODEIS", "%s %s" % (nick, self.user.get_mode()))
				return


		# Set mode
		cmds = args[0]
		state = ""

		for char in cmds:
			if char in "+-":
				state = char
			else:
				if nick[0] in "#&":
					# Channel
					if char == "b":
						chan.set_banmask(banmask=args[1])
					elif char == "l":
						chan.set_limit(user=args[2], limit=args[1])
					elif char == "v":
						chan.set_speak(user=args[1], value=state=="+")
					elif char == "o":
						chan.set_moderator(user=args[1], value=state=="+")
					elif char == "p":
						chan.set_private(value=state=="+")
					elif char == "s":
						chan.set_secret(value=state=="+")
					elif char == "i":
						chan.set_invite(value=state=="+")
					elif char == "t":
						chan.set_topic_by_operator(value=state=="+")
					elif char == "m":
						chan.set_moderated(value=state=="+")
					else:
						self.error("ERR_UNKNOWNMODE", "")
				else:
					# User
					if char == "i":
						self.user.set_invisible(value=state=="+")
					elif char == "s":
						self.user.set_receipt_server_notices(value=state=="+")
					elif char == "w":
						self.user.set_wallops(value=state=="+")
					elif char == "o":
						if state == "-" or self.user.is_moderator():
							self.user.set_moderator(value=state=="+")
					else:
						self.error("ERR_UNKNOWNMODE", "")

				state = ""

	def commandPrivmsg(self, receivers, message):
		receivers = receivers.split(",")

		for to in receivers:
			if to[0] in "#&":
				# Public message to channel
				chan = self.get_channel(to)
				chan.send(self.nick, message)
			else:
				# Private message
				user = User(to)
				user.send(self.nick, message)