class Channel(object):
	def __init__(self, name, key=None):
		self.name = name
		self.key = key

	def get_topic(self):
		return None

	def get_online(self):
		return []

	def get_user(self, nick):
		raise NotImplementedError()