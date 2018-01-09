from config import zeronet_directory
from zerowebsocket import ZeroWebSocket
import json, os

class ThunderWave(object):
	def __init__(self):
		self.address = "1CWkZv7fQAKxTVjZVrLZ8VHcrN6YGGcdky"

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