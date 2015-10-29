#!/usr/bin/env python 
import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        self.request.send("please send us your team ip\n")
        team = self.request.recv(1024).strip()
        self.request.send("please send us the flag\n")
        flag = self.request.recv(1024).strip()
        ff = open(team+"My.flag", "r")
        flags=[]
        for flag in ff.readlines():
            flags.append(flag)
        if flag in flags:
            ff = open(team+".off", "a")
            ff.write("+")
            ff.close()
            self.request.send("scored")
        ff.close()
        print flag
        

def submitserver(port):
    HOST, PORT = "0.0.0.0", port

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    print "Starting submit server on port " + str(PORT) + "\n"
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
