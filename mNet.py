#import required modules
import socket
import hashlib

#connection constants
checksum_size = 4

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
                check = data[len()]data[len(self.user_id):]

        #print connection request
        print(request)

    #connect to a listening user
    def connect(self, other_id):
        #set connection user
        self.other_id = other_id

        #send connection request
        self.server.sendto(other_id + b'hello world', self.address)

    #pack and send packet
    def send(self, msg):
        #add message data to message
        data = b'\x01\x02\x03'+ msg
        self.server.sendto(self.other_id + self.checksum(data) + self.encrypt(data))

    #encrypt the data
    def encrypt(self, data):
        return data

    #decrypt the data
    def decrypt(self, data):
        return data

    #calculate the checksum of bytes
    def checksum(self, data):
        #run checksum opperation
        sha = hashlib.sha256()
        sha.digest_size = checksum_size
        sha.update(data)
        return sha.digest()
