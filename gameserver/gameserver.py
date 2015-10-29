import hashlib
import random
import string
import time
import threading
import sys

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


##
# Get random string
##
def randomString(n):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))


def updateDefencePoints():
    global team, ff, flag
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
    global team, flag, ff
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


def createTeamFiles():
    global teams, team, ff
    fo = open("teams.list", "r")
    teams = []
    for team in fo.readlines():
        teams.append(team[:-1])
        ff = open(team[:-1] + "My.flag", "a")
        ff.close()


# Make threads for submitserver and scoreboard
submit_thread = submitThread(1, "submit_thread")
scoreboard_thread = scoreboardThread(2, "scoreboard_thread")

submit_thread.daemon = True
scoreboard_thread.daemon = True

submit_thread.start()
scoreboard_thread.start()

#update gameserver every minute
while True:
    createTeamFiles()

    PlaceTrolololFlags()

    time.sleep(60)

    updateDefencePoints()