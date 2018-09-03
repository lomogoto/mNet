#import required modules
import socket

#class for a connection
class Connection:
    #initialize connection with
    def __init__(self, username, matchmaking_address = ('FF1E::FF1E', 5151)):
        #save options
        self.user_id = username
        self.address = matchmaking_address

        #make sockets
        self.server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.client = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

        #set up sockets
        self.server.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, b'\xFF\x00\x00\x00')
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.bind(('', self.address[1]))
        self.switch_group(self.address[0])

    #connect to a group
    def switch_group(self, group):
        #try to leave the current group
        try:
            self.client.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_LEAVE_GROUP, self.mreq)
        except AttributeError:
            pass

        #connect to new group
        self.mreq = socket.inet_pton(socket.AF_INET6, group) + b'\x00\x00\x00\x00'
        self.client.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, self.mreq)

    #listen for connection
    def listen(self):
        #get data that matches address
        request = None
        while request == None:
            #get data from to parse
            data, address = self.client.recvfrom(1024)

            #check if request for this user
            if self.user_id == data[:len(self.user_id)]:
                request = data[len(self.user_id):]

        #print connection request
        print(request)

    #connect to a listening user
    def connect(self, other_id):
        #send connection request
        self.server.sendto(other_id + b'hello world', self.address)
