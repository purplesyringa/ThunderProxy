from util import debug, critical, ServerError, CommandError
import time

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
			self.recvall()