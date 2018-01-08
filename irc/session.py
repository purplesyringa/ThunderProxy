from util import debug, critical, ServerError, CommandError
from util import replycodes, errorcodes
import time, re

class Session(object):
	def __init__(self, conn, Channel):
		self.conn = conn
		self.channels = []
		self.Channel = Channel
		self.nick = "*"
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
		debug("New session")

		while True:
			message = self.recvall()
			if message.strip() == "":
				continue

			if message == "QUIT":
				break

			message = self.parseMessage(message)

			command = message["command"][0].upper() + message["command"][1:].lower()
			command = "command" + command

			if command in dir(self):
				getattr(self, command)(*message["params"])
			else:
				self.error("ERR_UNKNOWNCOMMAND", message["command"])

	def parseMessage(self, message):
		prefix = None
		if message[0] == ":":
			prefix = message[1:message.index(":")]
			message = message[message.index(":")+1:]

		message = re.split(r" +", message, maxsplit=1)

		command = message[0]

		if len(message) == 1:
			return dict(command=command, params=[])

		params = message[1]

		trailing = None
		try:
			index = params.index(":")
			trailing = params[index+1:]
			params = params[:index]
		except ValueError:
			pass

		params = re.split(r" +", params)
		if trailing is not None:
			params.append(trailing)

		return dict(command=command, params=params)

	def commandNick(self, nick):
		self.nick = nick

	def commandUser(self, username, hostname, servername, realname):
		self.username = username
		self.hostname = hostname
		self.servername = servername
		self.realname = realname

		self.ok(
			"RPL_WELCOME",
			":Welcome to the Internet Relay Network %s!%s@%s" % (self.nick, username, hostname)
		)

	def commandJoin(self, channels, keys=None):
		channels = channels.split(",")
		keys = keys.split(",") if keys is not None else []

		channels = map(None, channels, keys) # This is like zip() but with padding

		topic = None
		for channel in channels:
			chan = self.Channel(channel[0], key=channel[1])
			topic = chan.get_topic()
			self.channels.append(chan)

		if topic is None:
			self.ok("RPL_NOTOPIC", "")
		else:
			self.ok("RPL_TOPIC", ":%s" % topic)