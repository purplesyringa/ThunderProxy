from util import debug, critical, ServerError, CommandError
from util import replycodes, errorcodes
import re

class Transaction(object):
	def __init__(self, nick, username, hostname, conn, session, server):
		self.nick = nick
		self.username = username
		self.hostname = hostname
		self.user = server.register_user(nick, username, hostname, self)
		self.conn = conn
		self.session = session
		self.server = server
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
		self.ok("RPL_YOURHOST", ":Your host is localhost[127.0.0.1/6697], running version py-irc-1.0")
		self.ok("RPL_CREATED", ":This server was created Mon Jan 8 2018 at 2:55:16 EST")
		self.ok("RPL_MYINFO", "localhost py-irc-1.0 psitm iswo blvo")
		self.ok(
			"RPL_ISUPPORT",
			"PREFIX=(ov)@+ CHANTYPES=#& CHANMODES=eIbq,k,flj,CFLMPQScgimnprstz MODES=3 MAXCHANNELS=1000 CHANLIMIT=#&:1000 :are supported by this server"
		)
		self.ok(
			"RPL_ISUPPORT",
			"NICKLEN=1000 MAXBANS=1000 MAXLIST=beI:1000 NETWORK=ThunderWave CASEMAPPING=ascii ELIST=MN TOPICLEN=1000 :are supported by this server"
		)
		self.ok(
			"RPL_ISUPPORT",
			"KICKLEN=1000 CHANNELLEN=1000 AWAYLEN=1000 MAXTARGETS=1 :are supported by this server"
		)
		self.ok("RPL_LUSERCLIENT", ":There are 1 users and 0 invisible on 1 servers")
		self.ok("RPL_LUSEROP", "0 :IRC Operators online")
		self.ok("RPL_LUSERUNKNOWN", "0 :unknown connection(s)")
		self.ok("RPL_LUSERCHANNELS", "1 :channels formed")
		self.ok("RPL_LUSERME", ":I have 1 clients and 1 servers")
		self.ok("RPL_LOCALUSERS", "1 1 :Current local users 1, max 1")
		self.ok("RPL_GLOBALUSERS", "1 1 :Current global users 1, max 1")
		self.ok("RPL_STATSCONN", ":Highest connection count: 2 (1 clients) (1 connections received)")

	def commandJoin(self, channels, keys=None):
		channels = channels.split(",")
		keys = keys.split(",") if keys is not None else []

		channels = map(None, channels, keys) # This is like zip() but with padding

		for channel in channels:
			chan = self.server.get_channel(channel[0])
			if chan.get_key() != channel[1]:
				self.error("ERR_BADCHANNELKEY", "")

			chan.connect(self.user)
			self.user.join(chan)

			topic = chan.get_topic()
			self.ok("RPL_TOPIC", "%s :%s" % (channel[0], topic["topic"]))
			self.ok("RPL_TOPICWHOTIME", "%s %s %s" % (channel[0], topic["author"], int(topic["time"] / 1000)))

			# Specify online users
			online = [
				"@" + user.nick if user.is_admin() else
				"+" + user.nick if user.is_moderator() else
				user.nick

				for user in chan.get_online()
			]
			online = " ".join(online)

			self.ok("RPL_NAMREPLY", "@ %s :%s" % (channel[0], online))
			self.ok("RPL_ENDOFNAMES", "%s :End of /NAMES list." % channel[0])

			self.sendall(":%s!%s@%s JOIN %s" % (self.nick, self.username, self.hostname, channel[0]))

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
			chan = self.server.get_channel(channel)

			if len(args) == 0:
				# Send mode
				self.ok("RPL_CHANNELMODEIS", "%s %s" % (channel, chan.get_mode()))
				self.ok("RPL_CREATIONTIME", "%s %s" % (channel, int(chan.get_creation_time() / 1000)))
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
				chan = self.server.get_channel(to)
				chan.send(self.nick, self.username, message)
			else:
				# Private message
				self.server.get_user(to).send(self.nick, self.username, message)

	def commandUserhost(self, *users):
		replies = []
		for nick in users:
			user = self.server.get_user(nick)
			reply = ":%s%s=%s%s" % (nick, "*" if user.is_moderator() else "", "-" if user.is_away else "+", user.hostname)
			replies.append(reply)

		self.ok("RPL_USERHOST", " ".join(replies))

	def finish(self):
		channels = list(self.user.channels)
		for chan in channels:
			chan.disconnect(self.user)
			self.user.part(chan)
		self.user.disconnect(self)