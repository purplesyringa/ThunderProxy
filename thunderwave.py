from config import zeronet_directory
from zerowebsocket import ZeroWebSocket
import json, os, sqlite3

class ThunderWave(object):
	def __init__(self):
		self.address = "1CWkZv7fQAKxTVjZVrLZ8VHcrN6YGGcdky"

		self.conn = sqlite3.connect("%sdata/%s/data/ThunderWave2.db" % (zeronet_directory, self.address))
		self.cursor = self.conn.cursor()

	def listen_for_file_done(self, callback):
		# Find wrapper_key in sites.json
		wrapper_key = None
		with open(zeronet_directory + "data/sites.json", "r") as f:
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
		path = "%sdata/%s/data/users/%s/content.json" % (zeronet_directory, self.address, address)

		data = None
		with open(path, "r") as f:
			data = json.loads(f.read())

		return data["cert_user_id"]

	def get_lobby_messages(self, since=0):
		messages = self.cursor.execute("""
			SELECT
				key, date_added, body,
				json.cert_user_id,
				REPLACE(json.directory, "users/", "") AS from_address
			FROM messages

			LEFT JOIN json USING (json_id)

			WHERE date_added > ?
			ORDER BY date_added ASC
		""", (since,))

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