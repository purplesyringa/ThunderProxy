from channel import Channel
from user import User
import threading, re

import irc.server
server = irc.server.Server("localhost", 6697, Channel=Channel, User=User)
threading.Thread(target=server.serve).start()

from thunderwave import ThunderWave

lobby = server.get_channel("#lobby")

def callback(address):
	for message in tw.load_new_lobby_messages(address=address):
		lobby.broadcast(
			nick=message["cert_user_id"],
			username=re.sub(r"^(.*)@.*$", r"\1", message["from_address"]),
			message=message["body"]
		)

tw = ThunderWave()
tw.listen_for_file_done(callback)