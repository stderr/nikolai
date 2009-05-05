HOST = 'irc.freenode.net'
PORT = 6667
BOTNAME = 'hurrdurr'

# (channel name, password [optional])
CHANNELS = [
	('#reno.rb', ''),
	]

GREETING = 'hurr'

# All relevant commands that you want processed should start with this string
# Contained within the commands module
# Yea, MUDs and all that.  I've been a nerd for a while
COMMAND_PREFIX = 'do_'

# Local settings override
try:
    from local_settings import *
except ImportError:
    pass


