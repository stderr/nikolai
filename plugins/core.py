import urllib
try:
   import simplejson as json
except:
    print 'Failed to import simplejson'
 
 
command_prefix = 'do_'
 
def get_commands():
    return [v for k,v in globals().items() if k.startswith(command_prefix)]
 
def do_google(data):
    if data.has_key('google'):
        if data.addressed:
            if data.args:
                url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%(term)s" % { 'term' : urllib.quote(data.args) }
                response = json.load(urllib.urlopen(url))
                return data.reply("Total Results: %(total)s" % { 'total' : response['responseData']['cursor']['estimatedResultCount'] },
                                   (response['responseData']['results'][0]['url']))
 
def do_hello(data):
    if data.has_key('hello'):
        if data.addressed:
           return data.reply('Sup, %s.' % data.nick)
 
def do_help(data):
    """
    Provides a list of commands or help for a specific command
    [ if you don't want to incur runtime errors, keep this function at the bottom of the module ]
    """
    if data.has_key('help'):
        if data.args:
            pass
        else:
            bot._msg(data.reply, "List of commands:")
 
            for k,v in globals().items():
                if k.startswith(settings.COMMAND_PREFIX):
                    bot._msg(data.reply, "%s: %s" % (k[3:], v.__doc__))
