from channel import Channel
from user import User

import irc.server
server = irc.server.Server("localhost", 6697, Channel=Channel, User=User)
server.serve()