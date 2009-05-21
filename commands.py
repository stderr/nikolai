import settings

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
    Identified the user's host to the bot.
    """
    if data.addressed:
        if data.message.find('ident') != -1:
            if data.message.find(settings.PASSWORD) != -1:
                if ident(bot, data):
                    bot._msg(data.reply, 'Already identified')
                else:
                    bot.masters[data.host] = 1
                    bot._msg(data.reply, 'Successfully identified')
            else:
               bot._msg(data.reply, 'Incorrect password')

def do_reload_commands(bot, data):
    """
    Forces the bot to reload commands.py.
    """
    if data.addressed:
        if data.message.find('reload commands') != -1:
            if ident(bot, data):
                bot._reload_commands()
                bot._msg(data.reply, 'Commands reloaded')
            else:
                bot._msg(data.reply, 'You are not authorized to preform that operation')

def do_hello(bot, data):
    if data.addressed:
        if data.message.find('hello') != -1:
            bot._msg(data.reply, 'Sup, %s.' % data.nick)
            

def do_help(bot, data):
    """
        Provides a list of commands or help for a specific command
        [ if you don't want to incur runtime errors, keep this function at the bottom of the module ]
    """
    bot._msg(data.reply, "List of commands:")
    
    for k,v in globals().items():
        if k.startswith('do_'):
            bot._msg(data.reply, "%s: %s" % (k[3:], v.__doc__))
        
