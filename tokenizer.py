class Data(object):
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

