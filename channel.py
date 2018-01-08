class Channel(object):
	def __init__(self, name, key=None):
		self.name = name
		self.key = key

	def get_topic(self):
		return None