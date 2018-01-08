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

from enum import Enum
class errorcodes(Enum):
	ERR_NOSUCHNICK = 401, ":No such nick/channel"
	ERR_NOSUCHSERVER = 402, ":No such server"
	ERR_NOSUCHCHANNEL = 403, ":No such channel"
	ERR_CANNOTSENDTOCHAN = 404, ":Cannot send to channel"
	ERR_TOOMANYCHANNELS = 405, ":You have joined too many channels"
	ERR_WASNOSUCHNICK = 406, ":There was no such nickname"
	ERR_TOOMANYTARGETS = 407, ":Duplicate recipients. No message delivered"
	ERR_NOORIGIN = 409, ":No origin specified"
	ERR_NORECIPIENT = 411, ":No recipient given"
	ERR_NOTEXTTOSEND = 412, ":No text to send"
	ERR_NOTOPLEVEL = 413, ":No toplevel domain specified"
	ERR_WILDTOPLEVEL = 414, ":Wildcard in toplevel domain"
	ERR_UNKNOWNCOMMAND = 421, ":Unknown command"
	ERR_NOMOTD = 422, ":MOTD File is missing"
	ERR_NOADMININFO = 423, ":No administrative info available"
	ERR_FILEERROR = 424, ":File error doing"
	ERR_NONICKNAMEGIVEN = 431, ":No nickname given"
	ERR_ERRONEUSNICKNAME = 432, ":Erroneus nickname"
	ERR_NICKNAMEINUSE = 433, ":ERR_NICKNAMEINUSE"
	ERR_NICKCOLLISION = 436, ":Nickname collision KILL"
	ERR_USERNOTINCHANNEL = 441, ":They aren't on that channel"
	ERR_NOTONCHANNEL = 442, ":You're not on that channel"
	ERR_USERONCHANNEL = 443, ":is already on channel"
	ERR_NOLOGIN = 444, ":User not logged in"
	ERR_SUMMONDISABLED = 445, ":SUMMON has been disabled"
	ERR_USERSDISABLED = 446, ":USERS has been disabled"
	ERR_NOTREGISTERED = 451, ":You have not registered"
	ERR_NEEDMOREPARAMS = 461, ":Not enough parameters"
	ERR_ALREADYREGISTRED = 462, ":You may not reregister"
	ERR_NOPERMFORHOST = 463, ":Your host isn't among the privileged"
	ERR_PASSWDMISMATCH = 464, ":Password incorrect"
	ERR_YOUREBANNEDCREEP = 465, ":You are banned from this server"
	ERR_KEYSET = 467, ":Channel key already set"
	ERR_CHANNELISFULL = 471, ":Cannot join channel (+l)"
	ERR_UNKNOWNMODE = 472, ":is unknown mode char to me"
	ERR_INVITEONLYCHAN = 473, ":Cannot join channel (+i)"
	ERR_BANNEDFROMCHAN = 474, ":Cannot join channel (+b)"
	ERR_BADCHANNELKEY = 475, ":Cannot join channel (+k)"
	ERR_NOPRIVILEGES = 481, ":Permission Denied- You're not an IRC operator"
	ERR_CHANOPRIVSNEEDED = 482, ":You're not channel operator"
	ERR_CANTKILLSERVER = 483, ":You cant kill a server!"
	ERR_NOOPERHOST = 491, ":No O-lines for your host"
	ERR_UMODEUNKNOWNFLAG = 501, ":Unknown MODE flag"
	ERR_USERSDONTMATCH = 502, ":Cant change mode for other users"