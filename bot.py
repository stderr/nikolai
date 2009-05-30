import socket
import select
import settings
import functions
 
class Bot(object):
    def __init__(self):
        self.sockets = []
        self.nicks = {} #Replace this with a get_nicks() method
        self.commands = self.load_plugins()
        self.masters = {}
        self.password = settings.PASSWORD
        self.command_token = settings.COMMAND_TOKEN
 
    def connect(self):
        for network in settings.networks:
            sock = socket.socket()
            try:
                port = network['port']
            except:
                port = 6667
            sock.connect((network['host'], port))
 
            try:
                nick = network['nick']
            except:
                nick = settings.defaultNick
            self.handle_output(sock, 'NICK %s\r\n' % nick)
            #Should try altNick is user is in use.
            self.nicks[id(sock)] = nick #Replace this with get_nick()
 
            try:
                user = network['user']
            except:
                user = settings.defaultUser
            self.handle_output(sock, 'USER %s\r\n' % user)
 
            for channel in network['channels']:
                self.handle_output(sock, 'JOIN %s %s\r\n' % (channel[0], channel[1]))
 
            self.sockets.append(sock)
 
        while 1:
            read, write, exception = select.select(self.sockets,[],[])
            for sock in read:
                #try:
                data = sock.recv(4096)
                self.handle_input(sock, data)
                #except:
                #    print 'Something went wrong'
 
    def handle_input(self, sock, data):
        functions.handle_input(self, sock, data)
 
    def handle_output(self, sock, data):
        functions.handle_output(self, sock, data)
 
    def load_plugins(self):
        return functions.load_plugins(self)
 
    def reload_bot(self):
        reload(functions)
 
 
 
 
if __name__ == '__main__':
    bot = Bot()
    bot.connect()