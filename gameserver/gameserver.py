
import hashlib
import os
import random
import string
import time
import threading
import re

import trololol_put
import trololol_get
import scoreboard
import submitserver

class scoreboardThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "scoreboard starting..."
        scoreboard.scoreboard(9990)

class submitThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print "submit server starting..."
        submitserver.submitserver(9999)


def randomString(n):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))


def updateDefencePoints():
    global team
    print "updating def points"
    for team in teams:
        ff = open(team + "My.flag", "r")
        flag = ff.readlines()[-1:][0][:-1]
        ff.close()
        if trololol_get.trololol_get(team, flag):
            print "team " + str(team) + " won a defense point!"
            ff = open(team + ".def", "a")
            ff.write("+")
            ff.close()
        else:
            ff = open(team + ".def", "a")
            ff.write("-")
            ff.close()


def PlaceTrolololFlags():
    global team
    for team in teams:
        print team
        m = hashlib.md5()
        m.update(randomString(100))
        flag = m.hexdigest()
        trololol_put.trololol_put(team, flag)
        for otherteam in teams:
            if otherteam != team:
                ff = open(otherteam + ".flag", "a")
                ff.write(flag + "\n")
                ff.close()
            else:
                ff = open(otherteam + "My.flag", "a")
                ff.write(flag + "\n")
                ff.close()


def read_team_files():
    global teams

    ip4 = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

    fo = open("teams.list", "r")
    teams = []

    # Read times config file and append IP adress to teams array if it's valid.
    with open("teams.list", "r") as t:
        for team in t.read().splitlines():
            if ip4.match(team) is not None:
                teams.append(team[:-1])
                ff = open(team[:-1] + "My.flag", "a")
                ff.cose()
            else:
                print "[WARNING] " + team + " is not a valid IPv4 adress! team is excluded from CTF!"



def start_server_threads():
    # Make threads for submitserver and scoreboard
    submit_server_thread = submitThread(1, "submit_thread")
    scoreboard_server_thread = scoreboardThread(2, "scoreboard_thread")
    submit_server_thread.daemon = True
    scoreboard_server_thread.daemon = True
    submit_server_thread.start()
    scoreboard_server_thread.start()


def main():
    start_server_threads()

    read_team_files()

    #update gameserver every n seconds
    try:
        while True:

            PlaceTrolololFlags()

            time.sleep(30)

            updateDefencePoints()

    except KeyboardInterrupt:
        print "Shutting down..."




if __name__ == "__main__":
    main()
