import statbotics
import requests
import time
import threading
from tkinter import *



API_KEY = '1W5Sv6rdoO1MQPuw7f8cCtj580bgCbnyiGbaPFYUQqGWRtPk40OfkY7jyZehfimz'

sb = statbotics.Statbotics()
with open('teams.txt', 'r') as teams:
    teams = teams.read().split(' ')
        
def writeTeams():
    a = requests.get("https://www.thebluealliance.com/api/v3/event/2023mitr2/teams", headers={'X-TBA-Auth-Key':'A8ZBYBY2Sz9sJnrKjqskPpYognaDZxEWikowNRG2I400zPpVsVXL3tEk6zeW6lFr'}).json()
    print(a)
    with open('teams.txt', 'w') as teams:
        for x in a:
            teams.write(str(x['team_number']) + ' ')

def teamInfo(tNum, rank=False):
    if rank == True:
        x = sb.get_team_event(tNum, '2023mitr2')
        return x['epa_mean']
    else:
        x = sb.get_team_event(tNum, '2023mitr2')
        print(x)
        r = x['rank']
        eA = x['auto_epa_mean']
        eM = x['epa_mean']
        rp = x['rps']
        rpa = x['rps_per_match']
        rec = str(x['wins']) + ' - ' +  str(x['losses']) + ' - ' + str(x['ties'])
        print("Rank:", r)
        print("Record:", rec)
        print("Auto EPA:", eA)
        print("Total EPA:", eM)
        print("Average RP:", rpa)
        print("Total RP:", rp)

def opRankings():
    epar = {}
    for x in teams:
        try:
            eM = teamInfo(int(x), True)
            epar[int(x)] = eM
        except ValueError:
            pass
    sort = dict(sorted(epar.items(), key=lambda x:x[1], reverse=True))
    
    with open('eRank.txt', 'w') as x:
        words = ''
        for y in sort:
            words += str(y) + ': ' + str(sort[y]) + '\n'
        x.write(str(words))

    a = requests.get("https://www.thebluealliance.com/api/v3/event/2023mitr2/rankings", headers={'X-TBA-Auth-Key':'A8ZBYBY2Sz9sJnrKjqskPpYognaDZxEWikowNRG2I400zPpVsVXL3tEk6zeW6lFr'}).json()['rankings']
    words = ''
    for x in a:
        words += str(x['rank']) + ': ' + str(x['team_key']).removeprefix('frc') + '\n'
    with open('rank.txt', 'w') as y:
        y.write(words)


def matchChance(mNum):
    matches = sb.get_matches(event='2023mitr2')
    for x in matches:
        if x['match_number'] == mNum:
            mN = x['match_number']
            red_epa = x['red_epa_sum']
            blue_epa = x['blue_epa_sum']
            r1 = x['red_1']
            r2 = x['red_2']
            r3 = x['red_3']
            b1 = x['blue_1']
            b2 = x['blue_2']
            b3 = x['blue_3']
    try:
        print("Match Number:", mN)
        print("Red EPA:", red_epa)
        print("Blue EPA:", blue_epa, end='\n\n')
        print("Red Team 1:", r1)
        print("Red Team 2:", r2)
        print("Red Team 3:", r3, end='\n\n')
        print("Blue Team 1:", b1)
        print("Blue Team 2:", b2)
        print("Blue Team 3:", b3)
    except UnboundLocalError:
        print("Match not available.")

def compare():
    valueRank = {}
    for y in teams:
        try:
            x = sb.get_team_event(int(y), '2023mitr2')
            epa = x['epa_mean']
            rank = x['rank']
            rv = 2*rank
            val = abs(epa-rv)
            valueRank[y] = val
        except ValueError:
            print(y)
    sort = dict(sorted(valueRank.items(), key=lambda x:x[1], reverse=False))

    print(sort)
while True:
    x = input("Fetch team info, update ranking information, or get match info?\n")

    if x == '0':
        tn = int(input('Team Number: '))
        teamInfo(tn)
    elif x == '1':
        getRankings()
        opRankings()
    elif x == '2':
        mn = int(input("What is the match number?\n"))
        matchChance(mn)

    
    else:
        print('its 0 or 1 or 2 lol')