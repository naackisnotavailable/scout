from tkinter import *
from tkinter import ttk
import requests
import statbotics
from datetime import datetime



sb = statbotics.Statbotics()
with open('teams.txt', 'r') as teams:
    teams = teams.read().split(' ')
def offlineFind():
    with open('offlinesync.txt', 'r') as teaminfo:
        ti = dict(teaminfo.read())
        try:
            x = ti[5530]
            r = "Rank: " + str(x['rank'])
            eA = "Mean Auto EPA: " + str(x['auto_epa_mean'])
            eM = "Mean EPA: " + str(x['epa_mean'])
            rp = "Ranking Points: " + str(x['rps'])
            rpa = "Ranking Point Average: " + str(x['rps_per_match'])
            rec = "Record: " + str(x['wins']) + ' - ' +  str(x['losses']) + ' - ' + str(x['ties'])
            return (r, rec, eA, eM, rpa, rp)
            
        except KeyError as k:
            res = 'No data stored.'
    return (False, res)

print('hi')
def teamInfo(tNum, rank=False):
    if rank == True:
        x = sb.get_team_event(tNum, '2023mitr2')
        return x['epa_mean']
    else:
        x = sb.get_team_event(tNum, '2023mitr2')
        print(x)
        r = "Rank: " + str(x['rank'])
        eA = "Mean Auto EPA: " + str(x['auto_epa_mean'])
        eM = "Mean EPA: " + str(x['epa_mean'])
        rp = "Ranking Points: " + str(x['rps'])
        rpa = "Ranking Point Average: " + str(x['rps_per_match'])
        rec = "Record: " + str(x['wins']) + ' - ' +  str(x['losses']) + ' - ' + str(x['ties'])
        return (r, rec, eA, eM, rpa, rp)
def find(*args):
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
    except ValueError as v:
        print(v)
def update(*args):
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

root = Tk()
root.title("Team Finder")



mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
record1 = StringVar()
rank1 = StringVar()
rp1 = StringVar()
rpa1 = StringVar()
epaT1 = StringVar()
epaA1 = StringVar()
date = StringVar()



ttk.Button(mainframe, text="Find", command=find).grid(column=3, row=11, sticky=W)
ttk.Button(mainframe, text="Update data", command=update).grid(column=4, row=11, sticky=W)
ttk.Button(mainframe, text="Offline Find", command=offlineFind).grid(column=5, row=11, sticky=W)


ttk.Label(mainframe, textvariable=date).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=rank1).grid(column=2, row=4, sticky=(W, E))
ttk.Label(mainframe, textvariable=rp1).grid(column=2, row=5, sticky=(W, E))
ttk.Label(mainframe, textvariable=rpa1).grid(column=2, row=6, sticky=(W, E))
ttk.Label(mainframe, textvariable=epaT1).grid(column=2, row=7, sticky=(W, E))
ttk.Label(mainframe, textvariable=epaA1).grid(column=2, row=8, sticky=(W, E))

tn = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=tn)
feet_entry.grid(column=2, row=1, sticky=(W, E))

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