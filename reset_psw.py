#!/usr/bin/python
import json
import sys
import requests

def reset_psw(server, player, new_psw, root_psw):
    url = 'http://' + server + '/nhlplayoffs/api/v2.0/players/' + player + '/reset'
    headers = {'content-type': 'application/json'}
    data = {'new_psw':new_psw, 'root_psw':root_psw}
    r = requests.post(url, data = json.dumps(data), headers=headers)
    if not r.ok:
        print('Invalid request!!!!')
    if r.json()['result']:
        print('Reset successful')
    else:
        print('Invalid parameter')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('reset_psw.py <player> <new_psw> <root_psw>')
        exit(1)
    player = sys.argv[1]
    new_psw = sys.argv[2]
    root_psw = sys.argv[3]

    #server = 'localhost:5000'
    server = 'nhlpool.herokuapp.com/'
    reset_psw(server, player, new_psw, root_psw)
