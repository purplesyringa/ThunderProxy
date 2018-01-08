import irc.server
server = irc.server.Server("localhost", 6697)
server.serve()