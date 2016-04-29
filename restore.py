#!/usr/bin/python
import json
import sys
import requests

def restore(server, filename, root_psw):
    with open(filename, 'r') as infile:
        data = json.load(infile)

    url = 'http://' + server + '/nhlplayoffs/api/v2.0/restore'
    headers = {'content-type': 'application/json'}
    data = {'root_psw':root_psw, 'data':data}
    r = requests.post(url, data = json.dumps(data), headers=headers)
    if not r.ok:
        print('Invalid request!!!!')
        return False

    if r.json()['result']:
        print('Restore successful')
        return True
    else:
        print('Invalid parameter');
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('restore.py <filename> <root_psw>')
        exit(1)
    filename = sys.argv[1]
    root_psw = sys.argv[2]

    if len(sys.argv) > 3 and sys.argv[3] == 'prod':
        print('Using production server')
        server = 'nhlpool.herokuapp.com/'
    else:
        print('Using debug server')
        server = 'localhost:5000'

    restore(server, filename, root_psw)
