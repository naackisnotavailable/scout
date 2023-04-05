import requests

a = requests.get(f'https://www.thebluealliance.com/api/v3/district/2023fim/events', headers={'X-TBA-Auth-Key':'A8ZBYBY2Sz9sJnrKjqskPpYognaDZxEWikowNRG2I400zPpVsVXL3tEk6zeW6lFr'}).json()
for x in a:
    if x['city'] == 'Saline':
        print(x['event_code'])