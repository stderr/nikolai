import sys
import os
import re
 
class Tokenizer(object):
    def __init__(self, data, addressed, ident):
        """
        A slimmed down version of tokenizer.Data. data should be an re.match of
        a PRIVMSG
        """
        self.addressed = addressed
        self.ident = ident
 
        self.nick = data.group(1)
        self.username = data.group(2)
        self.host = data.group(3)
        self.channel = data.group(5)
        self.message = data.group(6)
 
        if self.channel.find("#") != -1:
            self.reply_to = self.channel
        else:
            self.reply_to = self.nick
 
    def has_key(self, key):
        """
        Returns True if self.message has key
        sets self.args to the string following key.
        """
        f = self.message.find(key)
        if f != -1:
            self.args = self.message[f+len(key)+1:]
            return True
 
    def reply(self, message):
        return 'PRIVMSG %s :%s\r\n' % (self.reply_to, message)
 
def handle_input(self, sock, data):
    """
    Replacement for Tokenizer.Data. There's so much shared functionality
    between Bot and Tokenizer.Data that it makes more sense to have parsing
    incoming messages be a method of Bot rather than passing Bot over every
    message.
    """
    print data
 
    if re.search('^:(.+)!(.+)@(.+) (.+) (.+) :(.+)$', data):
        m = re.search('^:(.+)!(.+)@(.+) (.+) (.+) :(.+)$', data)
 
        if data.find(self.nicks[id(sock)]) != -1:
            addressed = True
        elif data.split(':')[-1].find(self.command_token) == 0: #Should just use m.group(whatever)
            addressed = True
        else:
            addressed = False
 
        try:
            self.masters[m.group(3)] #host
            ident = True
        except:
            ident = False
 
        token = Tokenizer(m, addressed, ident)
 
        #ident and reload are the only two commands that should modify the bot.
        if token.addressed:
            if token.has_key('ident'):
                if not token.ident:
                    if token.args.find(self.password) != -1:
                        self.masters[token.host] = 1
                        self.handle_output(sock, token.reply('Successfully identified'))
                    else:
                        self.handle_output(sock, token.reply('Incorrect password'))
                else:
                    self.handle_output(sock, token.reply('Already identified'))
 
            elif token.has_key('reload'):
                if token.ident:
                    if token.args:
                        if token.args.find('plugins') != -1:
                            self.load_plugins()
                            self.handle_output(sock, token.reply('Plugins reloaded'))
 
                        elif token.args.find('bot') != -1:
                            self.reload_bot()
                            self.handle_output(sock, token.reply('Bot reloaded'))
                    else:
                        self.reload_bot()
                        self.load_plugins()
                        self.handle_output(sock, token.reply('Bot and plugins reloaded'))
 
        for command in self.commands:
            try:
                replies = command(token)
                if replies:
                    if type(replies) == type(''):
                        replies = (replies,)
                    for reply in replies:
                        self.handle_output(sock, reply)
            except:
                print 'Failed to run %s' % command
 
 
    elif re.search('^PING :(.*)$', data):
        self.handle_output(sock, 'PONG')
 
    #We aren't really doing anything with these last two but I'll keep them in.
    elif re.search('^:(.+) ([0-9]+) (.+)$', data):
        m = re.search('^:(.+) ([0-9]+) (.+)$', data)
        self.host = m.group(1)
        self.type = 'SERVMSG'
        self.code = m.group(2)
        self.message = m.group(3)
 
    else:
        self.type = 'OTHER'
 
def handle_output(self, sock, data):
    try:
        sock.send(data)
        print '>>> %s' % data
    except:
        'Failed to send: %s' % data
 
def load_plugins(self):
    """
    This should import all the .py files in /plugins and run module.get_commands()
    for each one. module.get_commands() returns a list of functions that gets
    added to self.commands
    """
    sys.path.append(os.path.join(sys.path[0], 'plugins'))
 
    commands = []
 
    plugins = os.listdir('plugins')
    for f in plugins:
        m = re.search('(.+)\.py$', str(f))
        if m:
            plugins.append(__import__(m.group(1)))
            reload(plugins[-1]) #Should only reload module if it's not imported.
            commands += plugins[-1].get_commands()
    return commands
