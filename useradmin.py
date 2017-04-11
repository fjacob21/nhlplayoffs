#!/usr/bin/python
import argparse
import datetime
import json
import sys
import requests

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
    if cmd == 'list':
        listusers(server)
    else:
        print('Invalid command!!!')
