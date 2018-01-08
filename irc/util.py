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
class replycodes(Enum):
	RPL_TRACELINK = 200
	RPL_TRACECONNECTING = 201
	RPL_TRACEHANDSHAKE = 202
	RPL_TRACEUNKNOWN = 203
	RPL_TRACEOPERATOR = 204
	RPL_TRACEUSER = 205
	RPL_TRACESERVER = 206
	RPL_TRACENEWTYPE = 208
	RPL_TRACECLASS = 209
	RPL_STATSLINKINFO = 211
	RPL_STATSCOMMANDS = 212
	RPL_STATSCLINE = 213
	RPL_STATSNLINE = 214
	RPL_STATSILINE = 215
	RPL_STATSKLINE = 216
	RPL_STATSQLINE = 217
	RPL_STATSYLINE = 218
	RPL_ENDOFSTATS = 219
	RPL_UMODEIS = 221
	RPL_SERVICEINFO = 231
	RPL_ENDOFSERVICES = 232
	RPL_SERVICE = 233
	RPL_SERVLIST = 234
	RPL_SERVLISTEND = 235
	RPL_STATSLLINE = 241
	RPL_STATSUPTIME = 242
	RPL_STATSOLINE = 243
	RPL_STATSHLINE = 244
	RPL_LUSERCLIENT = 251
	RPL_LUSEROP = 252
	RPL_LUSERUNKNOWN = 253
	RPL_LUSERCHANNELS = 254
	RPL_LUSERME = 255
	RPL_ADMINME = 256
	RPL_ADMINLOC1 = 257
	RPL_ADMINLOC2 = 358
	RPL_ADMINEMAIL = 259
	RPL_TRACELOG = 261
	RPL_NONE = 300
	RPL_AWAY = 301
	RPL_USERHOST = 302
	RPL_ISON = 303
	RPL_UNAWAY = 305
	RPL_NOWAWAY = 306
	RPL_WHOISUSER = 311
	RPL_WHOISSERVER = 312
	RPL_WHOISOPERATOR = 313
	RPL_WHOWASUSER = 314
	RPL_ENDOFWHO = 315
	RPL_WHOISCHANOP = 316
	RPL_WHOISIDLE = 317
	RPL_ENDOFWHOIS = 318
	RPL_WHOISCHANNELS = 319
	RPL_LISTSTART = 321
	RPL_LIST = 322
	RPL_LISTEND = 323
	RPL_CHANNELMODEIS = 324
	RPL_NOTOPIC = 331
	RPL_TOPIC = 332
	RPL_INVITING = 341
	RPL_SUMMONING = 342
	RPL_VERSION = 351
	RPL_WHOREPLY = 352
	RPL_NAMREPLY = 353
	RPL_KILLDONE = 361
	RPL_CLOSING = 362
	RPL_CLOSEEND = 363
	RPL_LINKS = 364
	RPL_ENDOFLINKS = 365
	RPL_ENDOFNAMES = 366
	RPL_BANLIST = 367
	RPL_ENDOFBANLIST = 368
	RPL_ENDOFWHOWAS = 369
	RPL_INFO = 371
	RPL_MOTD = 372
	RPL_INFOSTAR = 373
	RPL_ENDOFINFO = 374
	RPL_MOTDSTART = 375
	RPL_ENDOFMOTD = 376
	RPL_YOUREOPER = 381
	RPL_REHASHING = 382
	RPL_MYPORTIS = 384
	RPL_TIME = 391
	RPL_USERSSTART = 392
	RPL_USERS = 393
	RPL_ENDOFUSERS = 394
	RPL_NOUSERS = 395
	ERR_YOUWILLBEBANNED = 466
	ERR_BADCHANMASK = 476
	ERR_NOSERVICEHOST = 492

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