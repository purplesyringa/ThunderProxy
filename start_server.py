from channel import Channel
from user import User
import threading, re

import irc.server
server = irc.server.Server("localhost", 6667, Channel=Channel, User=User)
threading.Thread(target=server.serve).start()

from thunderwave import Singleton as ThunderWave

lobby = server.get_channel("#lobby")

def callback(address):
	for message in tw.load_new_lobby_messages(address=address):
		user = server.register_user(
			nick=message["cert_user_id"].replace("@", "/"),
			username=message["from_address"],
			hostname="remote"
		)

		lobby.receiveMsg(
			user=user,
			message=message["body"].replace("\n", "\r\n")
		)

tw = ThunderWave()
tw.listen_for_file_done(callback)