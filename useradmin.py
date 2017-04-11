#!/usr/bin/python
import argparse
import datetime
import json
import sys
import requests


def removeuser(server, user, root_psw):
    try:
        url = 'http://' + server + '/nhlplayoffs/api/v2.0/players/'+user
        headers = {'content-type': 'application/json'}
        data = {'root_psw':root_psw}
        r = requests.delete(url, data = json.dumps(data), headers=headers)
        if not r.ok:
            print('Invalid request!!!!')
            return False
        if r.json()['result']:
            print('Remove {0} successful'.format(user))
            return True
        else:
            print('Invalid parameter');
            return False
    except Exception as e:
        print(e)
        return False

def listusers(server):
    try:
        url = 'http://' + server + '/nhlplayoffs/api/v2.0/players'
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        if not r.ok:
            print('Invalid request!!!!')
            return False
        players = r.json()['players']
        for player in players:
            print("\033[0;94m{n}\033[0m".format(n=player['name']))
            print("\t\033[1;30mEmail:\033[0m{e}".format(e=player['email']))
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage the nhlpool players')
    parser.add_argument('cmd', metavar='cmd',
                       help='The command to execute')
    parser.add_argument('user', metavar='user', default='', nargs='?',
                       help='The user')
    parser.add_argument('root_psw', metavar='password', default='', nargs='?',
                       help='The root password')
    parser.add_argument('-s', '--server', metavar='server', default='debug', nargs='?',
                       help='The server to use')

    args = parser.parse_args()

    if args.server == 'prod':
        print('Using production server')
        server = 'nhlpool.herokuapp.com/'
    else:
        print('Using debug server')
        server = 'localhost:5000'

    cmd = args.cmd
    user = args.user
    root_psw = args.root_psw
    if cmd == 'list':
        listusers(server)
    elif cmd == 'remove':
        removeuser(server, user, root_psw)
    else:
        print('Invalid command!!!')
