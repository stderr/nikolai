import socket
import settings
import re

class Data:
    def __init__(self, raw_data):
        self.raw = raw_data

        if re.search('^:(.+)!(.+)@(.+) (.+) (.+) :(.+)$', raw_data):
            m = re.search('^:(.+)!(.+)@(.+) (.+) (.+) :(.+)$', raw_data)
            self.nick = m.group(1)
            self.username = m.group(2)
            self.host = m.group(3)
            self.type = m.group(4)
            self.channel = m.group(5)
            self.message = m.group(6)
        
        elif re.search('^PING :(.*)$', raw_data):
            m = re.search('^PING :(.*)$', raw_data)
            self.host = m.group(1)
            self.type = 'PING'

        elif re.search('^:(.+) ([0-9]+) (.+)$', raw_data):
            m = re.search('^:(.+) ([0-9]+) (.+)$', raw_data)
            self.host = m.group(1)
            self.type = 'SERVMSG'
            self.code = m.group(2)
            self.message = m.group(3)

        else:
            self.type = 'OTHER'

    def __repr__(self):
        return self.raw


class Bot(object):
    def __init__(self, **args):
        self.autojoin = args.get('autojoin', True)
        self.greet = args.get('greet', True)
        
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        
    def connect(self):
        """ 
            Connects to the specified host in settings.py and, optionally, joins all channels
        """
        
        self.irc.connect((settings.HOST, settings.PORT))
        
        print self.irc.recv(4096)
        
        self.irc.send("NICK %s\r\n" % (settings.BOTNAME,))
        self.irc.send("USER py py py py py bot\r\n")
        
        if self.autojoin:
            for channel in settings.CHANNELS:
                self._join(channel[0])
        
        if self.greet:
            for channel in settings.CHANNELS:
                self._msg(channel[0], settings.GREETING)
        
        while True:
            data = Data(self.irc.recv(4096))

            if data.type == "PRIVMSG":
               for command in self._get_commands():
                   command(self, data.message)
            
            elif data.type == "PING":
                self._send("PONG")

            print data

    def _send(self, data):
        """
        Sends data to the server
        """
        self.irc.send(data)
        print '>>> %s' % data
    
    def _msg(self, channel, text):
        """ 
        Channel message
        """
        self._send("PRIVMSG %s :%s\r\n" % (channel, text))
    
    def _join(self, channel, password=''):
        """
        Join a channel
        """
        self._send("JOIN %s %s\r\n" % (channel,password))
    
    def _get_commands(self):
        """
        Get all commands to respond to
        """
        import types, commands
       
        return [v for k,v in commands.__dict__.items() if type(v) is types.FunctionType and k.startswith(settings.COMMAND_PREFIX)]
        

if __name__ == '__main__':
    bot = Bot()
    bot.connect()
