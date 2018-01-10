from thunderwave import ThunderWave
import datetime

tw = ThunderWave()

messages = tw.get_lobby_messages()
messages.sort(key=lambda x: x["date_added"])
for message in messages:
	dt = datetime.datetime.fromtimestamp(message["date_added"] / 1000)

	print "%s (%s)" % (message["cert_user_id"], message["from_address"])
	print "[%s]" % message["key"]
	print dt.strftime("%Y-%m-%d %H:%M")
	print ""
	print message["body"].encode("utf-8")
	print ""
	print "----------------------------------------"
	print ""