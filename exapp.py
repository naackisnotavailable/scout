from tkinter import *
from tkinter import ttk
import requests
import statbotics
from datetime import datetime
import json
import webbrowser

encode = json.JSONEncoder()
decode = json.JSONDecoder()

sb = statbotics.Statbotics()

def callback(url):
   webbrowser.open_new_tab(url)


def writeTeams():
    mC = False
    a = requests.get(f'https://www.thebluealliance.com/api/v3/event/{eidc}/teams', headers={'X-TBA-Auth-Key':'A8ZBYBY2Sz9sJnrKjqskPpYognaDZxEWikowNRG2I400zPpVsVXL3tEk6zeW6lFr'}).json()
    print(a)
    with open('teams.txt', 'w') as teams:
        for x in a:
            teams.write(str(x['team_number']) + ' ')

def matchChance(*args):
    matches = sb.get_matches(event=eidc)
    print('mtch\n' + str(matches))
    for x in matches:
        if x['match_number'] == int(mN.get()):
            red_epa.set(x['red_epa_sum'])
            blue_epa.set(x['blue_epa_sum'])
            r1.set(x['red_1'])
            r2.set(x['red_2'])
            r3.set(x['red_3'])
            b1.set(x['blue_1'])
            b2.set(x['blue_2'])
            b3.set(x['blue_3'])

            red_epa.set("Red EPA: " + red_epa.get())
            blue_epa.set("Blue EPA: " + blue_epa.get())
            r1.set("Red Team 1: " + r1.get())
            r2.set("Red Team 2: " + r2.get())
            r3.set("Red Team 3: " + r3.get())
            b1.set("Blue Team 1: " + b1.get())
            b2.set("Blue Team 2: " + b2.get())
            b3.set("Blue Team 3: " + b3.get())

            ttk.Label(mainframe, textvariable=red_epa).grid(column=2, row=3, sticky=(W, E))
            ttk.Label(mainframe, textvariable=blue_epa).grid(column=2, row=4, sticky=(W, E))

            ttk.Label(mainframe, textvariable=blank_spot).grid(column=2, row=5, sticky=(W, E))

            ttk.Label(mainframe, textvariable=r1).grid(column=2, row=6, sticky=(W, E))
            ttk.Label(mainframe, textvariable=r2).grid(column=2, row=7, sticky=(W, E))
            ttk.Label(mainframe, textvariable=r3).grid(column=2, row=8, sticky=(W, E))

            ttk.Label(mainframe, textvariable=blank_spot).grid(column=2, row=9, sticky=(W, E))

            ttk.Label(mainframe, textvariable=b1).grid(column=2, row=10, sticky=(W, E))
            ttk.Label(mainframe, textvariable=b2).grid(column=2, row=11, sticky=(W, E))
            ttk.Label(mainframe, textvariable=b3).grid(column=2, row=12, sticky=(W, E))
            
            mC = True

with open('teams.txt', 'r') as teams:
    teams = teams.read().split(' ')


def eidup(*args):
    with open('event_id.txt', 'w') as f:
        f.write(idup.get())

def offlineFind():
    mC = False
    with open('offlinesync.json', 'r') as teaminfo:
        x = json.load(teaminfo)
        print(x)
        try:
            x = x[tn.get()]
            r = str(x['r'])
            eA = str(x['eA'])
            eM = str(x['eM'])
            rp = str(x['rp'])
            rpa = str(x['rpa'])
            rec = str(x['rec'])
            record1.set(rec)
            rank1.set(r)
            rp1.set(rp) 
            rpa1.set(rpa) 
            epaT1.set(eM) 
            epaA1.set(eA) 
            return (r, rec, eA, eM, rpa, rp)
            
        except Exception as k:
            res = 'No data stored.'
            print(k)
            print(res)
    return (False, res)



print('hi')
def teamInfo(tNum, rank=False):
    mc = False
    if rank == True:
        x = sb.get_team_event(tNum, eidc)
        return x['epa_mean']
    else:
        x = sb.get_team_event(tNum, eidc)
        print(x)
        r = "Rank: " + str(x['rank'])
        eA = "Mean Auto EPA: " + str(x['auto_epa_mean'])
        eM = "Mean EPA: " + str(x['epa_mean'])
        rp = "Ranking Points: " + str(x['rps'])
        rpa = "Ranking Point Average: " + str(x['rps_per_match'])
        rec = "Record: " + str(x['wins']) + ' - ' +  str(x['losses']) + ' - ' + str(x['ties'])
        return (r, rec, eA, eM, rpa, rp)
def find(*args):
    mC = False
    try:
        value = int(tn.get())
        (r, rec, eA, eM, rpa, rp) = teamInfo(value)
        record1.set(rec)
        rank1.set(r)
        rp1.set(rp) 
        rpa1.set(rpa) 
        epaT1.set(eM) 
        epaA1.set(eA) 
        date.set(str(datetime.now()))
        with open('offlinesync.json', 'r') as ols:
            cDict = json.load(ols)
        data = {}
        data['r'] = r
        data['rec'] = rec
        data['eA'] = eA
        data['eM'] = eM
        data['rpa'] = rpa
        data['rp'] = rp
        cDict[value] = data
        cDict = encode.encode(cDict)
        with open('offlinesync.json', 'w') as ols:
            json.dump(obj=cDict, fp=ols)

        with open('offlinesync.json', 'w') as ols:
            ols.write(str(cDict))
    except ValueError as v:
        print(v)
    

    try:
        a = requests.get(f'https://www.thebluealliance.com/api/v3/team/frc{tn.get()}', headers={'X-TBA-Auth-Key':'A8ZBYBY2Sz9sJnrKjqskPpYognaDZxEWikowNRG2I400zPpVsVXL3tEk6zeW6lFr'}).json()['website']
    except KeyError:
        pass
    if a == None:
        print('anone')
        noweb.set("No Website Available.")
        ttk.Label(mainframe, textvariable=noweb).grid(column=4, row=9, sticky=(W, E))
        link = Label(root, text="",font=('Helveticabold', 15), fg="blue", cursor="hand2")
        link.grid(column=4, row=9, sticky=(W, E))
        link.bind("<Button-1>", lambda e: callback(a))
    else:
        foo = StringVar()
        foo.set("")
        ttk.Label(mainframe, textvariable=foo).grid(column=4, row=10, sticky=(W, E))
        link = Label(root, text="Website",font=('Helveticabold', 5), fg="blue", cursor="hand2")
        link.grid(column=4, row=9, sticky=(W, E))
        link.bind("<Button-1>", lambda e: callback(a))
        
def update(*args):
    writeTeams()
    mC = False
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

    a = requests.get(f'https://www.thebluealliance.com/api/v3/event/{eidc}/rankings', headers={'X-TBA-Auth-Key':'A8ZBYBY2Sz9sJnrKjqskPpYognaDZxEWikowNRG2I400zPpVsVXL3tEk6zeW6lFr'}).json()['rankings']
    words = ''
    for x in a:
        words += str(x['rank']) + ': ' + str(x['team_key']).removeprefix('frc') + '\n'
    with open('rank.txt', 'w') as y:
        y.write(words)

root = Tk()
root.title("Team Finder")
mC = False




mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
record1 = StringVar()
rank1 = StringVar()
rp1 = StringVar()
rpa1 = StringVar()
epaT1 = StringVar()
epaA1 = StringVar()
date = StringVar()
noweb = StringVar()

red_epa = StringVar()
blue_epa = StringVar()
r1 = StringVar()
r2 = StringVar()
r3 = StringVar()
b1 = StringVar()
b2 = StringVar()
b3 = StringVar()

blank_spot = StringVar()
blank_spot.set(" ")

with open('event_id.txt', 'r') as eid:
    eidc = eid.read()


ttk.Button(mainframe, text="Find", command=find).grid(column=3, row=13, sticky=W)
ttk.Button(mainframe, text="Update data", command=update).grid(column=4, row=13, sticky=W)
ttk.Button(mainframe, text="Offline Find", command=offlineFind).grid(column=5, row=13, sticky=W)

ttk.Button(mainframe, text="Update Event ID", command=eidup).grid(column=10, row=13, sticky=W)
ttk.Button(mainframe, text="Get Match", command=matchChance).grid(column=12, row=13, sticky=W)

ttk.Label(mainframe, textvariable=date).grid(column=4, row=4, sticky=(W, E))
ttk.Label(mainframe, textvariable=rank1).grid(column=4, row=4, sticky=(W, E))
ttk.Label(mainframe, textvariable=rp1).grid(column=4, row=5, sticky=(W, E))
ttk.Label(mainframe, textvariable=rpa1).grid(column=4, row=6, sticky=(W, E))
ttk.Label(mainframe, textvariable=epaT1).grid(column=4, row=7, sticky=(W, E))
ttk.Label(mainframe, textvariable=epaA1).grid(column=4, row=8, sticky=(W, E))



mN = StringVar()
tn = StringVar()
idup = StringVar()
mN.set(0)

abc = ttk.Entry(mainframe, width=7, textvariable=tn)
abc.grid(column=2, row=1, sticky=(W, E))

hi = ttk.Entry(mainframe, width=7, textvariable=mN)
hi.grid(column=12, row=10, sticky=(W, E))
print('mn\n' + mN.get())

defg = ttk.Entry(mainframe, width=7, textvariable=idup)
defg.grid(column=10, row=10, sticky=(W, E))


root.mainloop()

#root = Tk()
#root.title("Feet to Meters")
#
#mainframe = ttk.Frame(root, padding="3 3 12 12")
#mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
#root.columnconfigure(0, weight=1)
#root.rowconfigure(0, weight=1)
#
#feet = StringVar()
#feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
#feet_entry.grid(column=2, row=1, sticky=(W, E))
#
#meters = StringVar()
#ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
#
#ttk.Button(mainframe, text="Find", command=calculate).grid(column=3, row=3, sticky=W)
#
#ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
#ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
#ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
#
#for child in mainframe.winfo_children(): 
#    child.grid_configure(padx=5, pady=5)
#
#feet_entry.focus()
#root.bind("<Return>", calculate)
#
#root.mainloop()