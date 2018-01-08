def debug(s, *args):
	if isinstance(s, basestring):
		print "[irc ] [debug   ] %s" % (s % args)
	else:
		print "[irc ] [debug   ] %s" % s

def critical(s, *args):
	if isinstance(s, basestring):
		print "[irc ] [critical] %s" % (s % args)
	else:
		print "[irc ] [critical] %s" % s


class ServerError(Exception):
	pass
class CommandError(Exception):
	pass