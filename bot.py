import socket
import re
import settings
from tokenizer import Data



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
                   command(self, data)
            
            elif data.type == "PING":
                self._send("PONG")

            print data

    def _send(self, data):
        """
        Sends data to the server with a printout.
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