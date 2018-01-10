import socket, traceback, threading
from util import debug, critical, ServerError
from connection import Connection
from session import Session

class Server(object):
	def __init__(self, host, port, Channel, User):
		self.host = host
		self.port = port
		self.Channel = Channel
		self.User = User
		self.sock = None
		self.sessions = []
		self.channels = []

	def serve(self):
		if self.sock is not None:
			raise ServerError("Socket already used")

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))
		try:
			debug("Serving")
			while True:
				self.sock.listen(1)
				conn, addr = self.sock.accept()

				thread = threading.Thread(target=self.run, args=(conn,))
				thread.daemon = True
				thread.start()
		except (SystemExit, KeyboardInterrupt):
			debug("Server quit")
		except Exception as e:
			critical(traceback.format_exc())
		finally:
			self.sock.shutdown(socket.SHUT_RDWR)
			self.sock.close()
			self.sock = None

	def run(self, conn):
		session = None
		try:
			conn = Connection(conn)
			session = Session(conn, User=self.User, server=self, auto_init=False)
			self.sessions.append(session)
			session.init()
		finally:
			try:
				self.sessions.remove(session)
			except ValueError:
				pass

			conn.close()

	def broadcast(self, nick, username, to, message):
		for session in self.sessions:
			print "broadcast to session", session
			session.broadcast(nick, username, to, message)

	def get_channel(self, channel):
		try:
			return next(chan for chan in self.channels if chan.name == channel)
		except StopIteration:
			chan = self.Channel(channel)
			self.channels.append(chan)
			return chan

	def has_channel(self, channel):
		try:
			next(chan for chan in self.channels if chan.name == channel)
			return True
		except StopIteration:
			return False