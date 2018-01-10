from config import data_directory
from zerowebsocket import ZeroWebSocket
import json, os, sqlite3, time, errno

current_directory = os.path.dirname(os.path.realpath(__file__))


class ThunderWave(object):
	def __init__(self):
		self.address = "1CWkZv7fQAKxTVjZVrLZ8VHcrN6YGGcdky"

		self.conn = sqlite3.connect("%s/%s/data/ThunderWave2.db" % (data_directory, self.address))
		self.cursor = self.conn.cursor()

		self.cache_directory = current_directory + "/cache"
		try:
			os.makedirs(self.cache_directory)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise

		self.update_cache_time()

	def listen_for_file_done(self, callback):
		# Find wrapper_key in sites.json
		wrapper_key = None
		with open(data_directory + "/sites.json", "r") as f:
			sites = json.loads(f.read())
			wrapper_key = sites[self.address]["wrapper_key"]

		# Access WebSocket
		with ZeroWebSocket(wrapper_key) as ws:
			ws.async("channelJoin", "siteChanged")

			while True:
				msg = ws.recv()
				if msg["cmd"] != "setSiteInfo":
					continue

				if "event" not in msg["params"] or msg["params"]["event"][0] != "file_done":
					continue

				file = msg["params"]["event"][1]
				if not file.startswith("data/users/"):
					continue

				address = (
					file
						.replace("data/users/", "")
						.replace("/content.json", "")
						.replace("/data.json", "")
						.replace("/data_private.json", "")
				)

				callback(address)

	def get_cert_user_id(self, address):
		path = "%s/%s/data/users/%s/content.json" % (data_directory, self.address, address)

		data = None
		with open(path, "r") as f:
			data = json.loads(f.read())

		return data["cert_user_id"]

	def get_lobby_messages(self, address=None, since=0):
		messages = self.cursor.execute("""
			SELECT
				key, date_added, body,
				json.cert_user_id,
				REPLACE(json.directory, "users/", "") AS from_address
			FROM messages

			LEFT JOIN json USING (json_id)

			WHERE date_added > ? AND %s
			ORDER BY date_added ASC
		""" % ("from_address = ?" if address is not None else "1 = 1"), (since,) if address is None else (since, address))

		messages = [message for message in messages]

		new_messages = []
		for message in messages:
			message = dict(
				key=message[0],
				date_added=message[1],
				body=message[2],
				cert_user_id=message[3],
				from_address=message[4]
			)

			new_messages.append(message)
		messages = new_messages

		return messages

	def load_new_lobby_messages(self, address=None):
		last_time = dict()
		try:
			with open(self.cache_directory + "/last_time.json", "r") as f:
				last_time = json.loads(f.read())
		except IOError:
			pass

		since = None
		try:
			since = last_time[address]
		except KeyError:
			since = 0

		messages = self.get_lobby_messages(address=address, since=since)

		if messages != []:
			last_date_added = max([message["date_added"] for message in messages])
			last_time[address] = last_date_added

			with open(self.cache_directory + "/last_time.json", "w") as f:
				f.write(json.dumps(last_time))

		return messages

	def update_cache_time(self):
		last_time = dict()
		try:
			with open(self.cache_directory + "/last_time.json", "r") as f:
				last_time = json.loads(f.read())
		except IOError:
			pass

		messages = self.cursor.execute("""
			SELECT
				MAX(date_added) AS date_added,
				REPLACE(json.directory, "users/", "") AS address
			FROM messages

			LEFT JOIN json USING (json_id)
			GROUP BY json.json_id
		""")

		for message in messages:
			last_time[message[1]] = message[0]

		with open(self.cache_directory + "/last_time.json", "w") as f:
			f.write(json.dumps(last_time))