#import required modules
import socket
import hashlib

#connection constants
checksum_size = 32
message_count_size = 8

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
        #do nothing if not in a group yet
        except AttributeError:
            pass

        #connect to new group
        self.mreq = socket.inet_pton(socket.AF_INET6, group) + b'\x00\x00\x00\x00'
        self.client.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, self.mreq)

    #listen for connection
    def listen(self):
        #receive data addressed to connection
        self.recv()

    #connect to a listening user
    def connect(self, other_id):
        #set connection user
        self.other_id = other_id

        #send connection request
        self.send(b'hello world')

    #unpack and receive packet
    def recv(self):
        #wait for message addressed to you
        packet = None
        while packet == None:
            #get data to parse
            raw, address = self.client.recvfrom(1024)
            print(b'raw data: ' + raw)

            #check if name matches
            name = raw[:len(self.user_id)]
            if name == self.user_id:
                #check if data encoded correctly
                check = raw[len(self.user_id):len(self.user_id)+checksum_size]
                data = self.decrypt(raw[len(self.user_id)+checksum_size:])
                if check == self.checksum(data):
                    #check other things . . .
                    packet = data
            
                    print(b'packet: ' + packet)

    #pack and send packet
    def send(self, msg):
        #add message data to message
        data = b'' #empty packet
        data += self.message_number.to_bytes(8, byteorder = 'big') #return address
        data += self.mreq[:8]

        #add unencrypted header
        self.server.sendto(self.other_id + self.checksum(data) + self.encrypt(data), self.address)

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
        sha.update(data)
        return sha.digest()
