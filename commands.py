import settings

def do_hello(bot, data):
    if data.message.find('hello %s' % (settings.BOTNAME,)) != -1:
        bot._msg(data.channel, 'Sup, %s.' % data.nick)

def ident(bot, data):
    """
    Returns True if the user has identified their host to the bot.
    """
    try:
        bot.masters[data.host]
        return True
    except:
        return False

def do_ident(bot, data):
    """
    Identified the user's hot to the bot.
    """
    if data.message.find('ident') != -1:
        if data.message.find(settings.BOTNAME) != -1 or data.channel == settings.BOTNAME:
            if data.message.find(settings.PASSWORD) != -1:
                try:
                    bot.masters[data.host]
                    bot._msg(data.nick, 'Already identified')
                except:
                   bot.masters[data.host] = 1
                   bot._msg(data.nick, 'Successfully identified')
            else:
                bot._msg(data.nick, 'Incorrect password')

def do_reload_commands(bot, data):
    """
    Forces the bot to reload commands.py.
    """
    if data.message.find('reload commands') != -1:
        if data.channel == settings.BOTNAME:
            if ident(bot, data):
                bot._reload_commands()
                bot._msg(data.nick, 'Commands reloaded')
            else:
                bot._msg(data.nick, 'You are not authorized to preform that operation')
        elif data.message.find(settings.BOTNAME) != -1:
            if ident(bot, data):
                bot._reload_commands()
                bot._msg(data.channel, 'Commands reloaded, %s' % data.nick)
            else:
                bot._msg(data.channel, 'You are not authorized to preform that operation, %s' % data.nick)