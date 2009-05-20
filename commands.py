import settings

def do_hello(bot, data):
    if data.message.find('hello %s' % (settings.BOTNAME,)) != -1:
        for channel in settings.CHANNELS:
            bot._msg(channel[0], 'Sup, sup.')