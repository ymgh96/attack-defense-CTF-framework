import hashlib
import os
import random
import re
import string
import threading
import time

import scoreboard
import submitserver
import trololol_get
import trololol_put


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


def updateDefencePoints(teams):
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


def PlaceTrolololFlags(teams):
    for team in teams:
        # only run when a team is not disabled
        if not str(team).__contains__('d'):
            # create a flag and place it on the server
            m = hashlib.md5()
            m.update(randomString(100))
            flag = m.hexdigest()
            trololol_put.trololol_put(team, flag)
            # each team has a file like 192.168.56.104.flag which contains the enemy's flags.
            # every team also has a file like 192.168.56.104My.flag which contains their own flags.
            for opponent in teams:
                if not str(opponent).__contains__('d'):
                    if opponent != team:
                        ff = open(opponent + ".flag", "a")
                        ff.write(flag + "\n")
                        ff.close()
                    else:
                        ff = open(opponent + "My.flag", "a")
                        ff.write(flag + "\n")
                        ff.close()


def read_team_files(teams):
    """
    opens teams.list and filters out valid ips from that list. Adds valid ip to team list
    Also makes a ipMY.flag file for each valid team.
    :param teams: list of teams ip adresses
    :return:
    """
    ip4 = re.compile("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

    with open("teams.list", "r") as t:
        for team in t.read().splitlines():
            if ip4.match(team) is not None:
                teams.append(team)

            else:
                print "[WARNING] " + team + " is not a valid IPv4 adress! team is excluded from CTF!"


def check_teams_online(teams):
    """
    if a team is offline, a d gets appended to the end of the ip adress.
    other functions then skip this ip. and this ip will not get any defence or attack points.
    :param teams: list of team ip
    """
    for ip in teams:
        response = os.system("ping -q -c 1 -W 2 " + ip)
        if response != 0:
            print "[WARNING] " + ip + " is offline! Remove the device from the team list? [y] "
            inp = raw_input().lower()

            if inp in ('y', 'ye', 'yes', ''):
                teams.remove(ip)
                print "[MESSAGE] " + ip + " removed from active team list"
            else:
                print "[MESSAGE] " + ip + " disabled"
                teams[teams.index(ip)] = ip + "d"


def write_team_files(teams):
    for team in teams:
        if not str(team).__contains__('d'):
            eteamf = open("enabled_teams.list", "a")
            eteamf.write(team + "\n")
            eteamf.close()
            ff = open(team + "My.flag", "a")
            ff.close();
            print "[MESSAGE] Added " + team + " succesfully!"


def start_server_threads():
    """
    Make daemon for submitserver and scoreboard
    """
    submit_server_thread = submitThread(1, "submit_thread")
    scoreboard_server_thread = scoreboardThread(2, "scoreboard_thread")
    submit_server_thread.daemon = True
    scoreboard_server_thread.daemon = True
    submit_server_thread.start()
    scoreboard_server_thread.start()


def main():
    try:
        teams = []
        read_team_files(teams)
        check_teams_online(teams)
        write_team_files(teams)
        start_server_threads()

    # update gameserver every n seconds
        while True:

            PlaceTrolololFlags(teams)

            time.sleep(30)

            updateDefencePoints(teams)

    except KeyboardInterrupt:
        print "Shutting down..."




if __name__ == "__main__":
    main()
