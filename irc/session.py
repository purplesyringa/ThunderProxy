from util import debug, critical, ServerError, CommandError
from util import replycodes, errorcodes
from transaction import Transaction
import re

class Session(object):
	def __init__(self, conn, Channel, User, auto_init=True):
		self.conn = conn
		self.Channel = Channel
		self.User = User
		self.nick = "*"
		self.transaction = None

		if auto_init:
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

			transaction = self.transaction or self
			if command in dir(transaction):
				getattr(transaction, command)(*message["params"])
			elif command == "commandPing":
				self.commandPing(*message["params"])
			else:
				transaction.error("ERR_UNKNOWNCOMMAND", message["command"])

	def parseMessage(self, message):
		prefix = None
		if message[0] == ":":
			prefix = message[1:message.index(":")]
			message = message[message.index(":")+1:]

		message = re.split(r" +", message, maxsplit=1)

		command = message[0]

		if len(message) == 1:
			return dict(command=command, params=[])

		params = message[1].strip()

		trailing = None
		try:
			index = params.index(":")
			trailing = params[index+1:]
			params = params[:index].strip()
		except ValueError:
			pass

		params = re.split(r" +", params) if params != "" else []
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

		self.transaction = Transaction(
			self.nick, self.username, self.hostname,
			Channel=self.Channel, User=self.User,
			conn=self.conn
		)

	def commandPing(self, server):
		self.sendall(":localhost PONG localhost :%s" % server)