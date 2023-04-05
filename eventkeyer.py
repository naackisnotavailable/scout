import requests
import statbotics

a = requests.get(f'https://www.thebluealliance.com/api/v3/district/2023fim/events', headers={'X-TBA-Auth-Key':'A8ZBYBY2Sz9sJnrKjqskPpYognaDZxEWikowNRG2I400zPpVsVXL3tEk6zeW6lFr'}).json()
for x in a:
    if x['city'] == 'Saline':
        print(x['event_code'])

sb = statbotics.Statbotics()

a = sb.get_event('2023mitr2')
a = sb.get_matches(team=5530, event='2023mitr2')

print(a)