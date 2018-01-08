from util import debug, critical, ServerError, CommandError
import time, re

class Session(object):
	def __init__(self, conn):
		self.conn = conn
		self.init()

	def sendall(self, *args, **kwargs):
		return self.conn.sendall(*args, **kwargs)
	def recvall(self, *args, **kwargs):
		return self.conn.recvall(*args, **kwargs)

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
				getattr(command, self)(*args)

	def parseMessage(self, message):
		prefix = None
		if message[0] == ":":
			prefix = message[1:message.index(":")]
			message = message[message.index(":")+1:]

		message = re.split(r" +", message, maxsplit=1)

		command = message[0]

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

	def command