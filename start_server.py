from channel import Channel
from user import User
import threading

import irc.server
server = irc.server.Server("localhost", 6697, Channel=Channel, User=User)
threading.Thread(target=server.serve).start()

from thunderwave import ThunderWave

def callback(address):
	for message in tw.load_new_lobby_messages(address=address):
		server.broadcast(
			nick=message["cert_user_id"],
			username=message["from_address"],
			to="#lobby",
			message=message["body"]
		)

tw = ThunderWave()
tw.listen_for_file_done(callback)