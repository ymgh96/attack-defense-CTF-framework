#!/usr/bin/env python 
import SocketServer
import os

class ScoreboardHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
       fo = open("enabled_teams.list", "r")
       self.request.send("team      | off | def \n")
       teams=[]
       for team in fo.readlines():
           teams.append(team[:-1])
       for team in teams:
            deff = 0
            off = 0
            if os.path.isfile(team+".def"):
               ff = open(team+".def", "r")
               deff=ff.readline().count('+');
               deffminus = ff.readline().count('-')
               deff -= deffminus
               ff.close()
            if os.path.isfile(team+".off"):
               ff = open(team+".off", "r")
               off=ff.readline().count('+')
               ff.close()
            self.request.send(team+" | "+str(off)+" | "+str(deff)+"\n")
           

def scoreboard(PORT):
    HOST= "0.0.0.0"
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), ScoreboardHandler)
    print "scoreboard started on port " + str(PORT) + "\n"
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()