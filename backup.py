#!/usr/bin/python
import json
import sys
import requests

def backup(server, filename, root_psw):
    url = 'http://' + server + '/nhlplayoffs/api/v2.0/backup'
    headers = {'content-type': 'application/json'}
    data = {'root_psw':root_psw}
    r = requests.post(url, data = json.dumps(data), headers=headers)
    if not r.ok:
        print('Invalid request!!!!')
        return False
    with open(filename, 'w') as outfile:
        json.dump(r.json(), outfile, indent=4, sort_keys=True)
    print('Backup successful')
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('backup.py <filename> <root_psw>')
        exit(1)
    filename = sys.argv[1]
    root_psw = sys.argv[2]

    if len(sys.argv) > 3 and sys.argv[3] == 'prod':
        print('Using production server')
        server = 'nhlpool.herokuapp.com/'
    else:
        print('Using debug server')
        server = 'localhost:5000'

    backup(server, filename, root_psw)
