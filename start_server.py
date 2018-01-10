from channel import Channel
from user import User
import threading

import irc.server
server = irc.server.Server("localhost", 6697, Channel=Channel, User=User)
threading.Thread(target=server.serve).start()