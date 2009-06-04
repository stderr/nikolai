"""
Bot class and __main__ support
"""
import socket
import select
import settings
import functions
 
class Bot(object):
    """
    IRC bot class
    """
    def __init__(self):
        """
        init
        """
        self.sockets = []
        self.nicks = {} #Replace this with a get_nicks() method
        self.commands = self.load_plugins()
        self.masters = {}
        self.password = settings.PASSWORD
        self.command_token = settings.COMMAND_TOKEN
 
    def connect(self):
        """
        connect to networks and channels in settings.py, and maintain connection
        """
        for network in settings.networks:
            sock = socket.socket()
            try:
                port = network['port']
            except KeyError:
                port = 6667
            sock.connect((network['host'], port))
 
            try:
                nick = network['nick']
            except KeyError:
                nick = settings.defaultNick
            self.handle_output(sock, 'NICK %s\r\n' % nick)
            #Should try altNick is user is in use.
            self.nicks[id(sock)] = nick #Replace this with get_nick()
 
            try:
                user = network['user']
            except KeyError:
                user = settings.defaultUser
            self.handle_output(sock, 'USER %s\r\n' % user)
 
            for channel in network['channels']:
                self.handle_output(sock, 'JOIN %s %s\r\n' % (channel[0], 
                                                            channel[1]))
 
            self.sockets.append(sock)
 
        while 1:
            read, write, exception = select.select(self.sockets, [], [])
            for sock in read:
                #try:
                data = sock.recv(4096)
                self.handle_input(sock, data)
                #except:
                #    print 'Something went wrong'
 
    def handle_input(self, sock, data):
        """
        pass off input handling
        """
        functions.handle_input(self, sock, data)
 
    def handle_output(self, sock, data):
        """
        pass off output handling
        """
        functions.handle_output(self, sock, data)
 
    def load_plugins(self):
        """
        load all plugins contained in plugins/
        """
        return functions.load_plugins(self)
 
    def reload_bot(self):
        """
        for hot reboots of plugins
        """
        reload(functions)
 
 
 
 
if __name__ == '__main__':
    bot = Bot()
    bot.connect()