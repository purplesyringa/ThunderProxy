from channel import Channel

import irc.server
server = irc.server.Server("localhost", 6697, Channel=Channel)
server.serve()