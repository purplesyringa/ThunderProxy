from util import debug, critical, ServerError, CommandError
from util import replycodes, errorcodes
import time, re

class Session(object):
	def __init__(self, conn):
		self.conn = conn
		self.init()

	def sendall(self, *args, **kwargs):
		return self.conn.sendall(*args, **kwargs)
	def recvall(self, *args, **kwargs):
		return self.conn.recvall(*args, **kwargs)

	def reply(self, code, nick, data):
		self.sendall(":localhost %s %s %s" % (code, nick, data))
	def error(self, code, nick, data):
		self.reply(errorcodes[code][0], nick, "%s %s" % (errorcodes[code][1], data))
	def ok(self, code, nick, data):
		self.reply(replycodes[code], nick, data)

	def init(self):
		debug("New session")

		while True:
			message = self.recvall()
			if message.strip() == "":
				continue

			message = self.parseMessage(message)

			command = message["command"][0].upper() + message["command"][1:].lower()
			command = "command" + command

			if command in dir(self):
				getattr(self, command)(*message["params"])
			else:
				self.error("ERR_UNKNOWNCOMMAND", "*", message["command"])

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
			self.nick,
			":Welcome to the Internet Relay Network %s!%s@%s" % (self.nick, username, hostname)
		)