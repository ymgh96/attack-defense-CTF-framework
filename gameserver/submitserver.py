#!/usr/bin/env python 
import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        self.request.send("please send us your team ip\n")
        team = self.request.recv(1024).strip()
        self.request.send("please send us the flag\n")
        flag = self.request.recv(1024).strip()

        ff = open(team+"My.flag", "r")
        flags=[]

        for flag in ff.readlines():
            flags.append(flag)
        ff.close()

        if flag in flags:

            sff = open(team+".found","r")
            foundFlags = sff.readlines()

            if flag in foundFlags:
                print "Already scored on flag!"
            else:
                # Write flag in teams found flag file
                sff.close()
                sff = open(team+".found","a")
                sff.write(flag+"\n")
                sff.close()
                # Add a score
                ff = open(team+".off", "a")
                ff.write("+")
                ff.close()
                self.request.send("scored")
        

def submitserver(port):
    HOST, PORT = "0.0.0.0", port

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    print "Starting submit server on port " + str(PORT) + "\n"
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
