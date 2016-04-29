#!/usr/bin/python
import argparse
import datetime
import json
import sys
import requests

def backup(server, filename, root_psw):
    try:
        url = 'http://' + server + '/nhlplayoffs/api/v2.0/backup'
        headers = {'content-type': 'application/json'}
        data = {'root_psw':root_psw}
        r = requests.post(url, data = json.dumps(data), headers=headers)
        if not r.ok:
            print('Invalid request!!!!')
            return False
        with open(filename, 'w') as outfile:
            json.dump(r.json(), outfile, indent=4, sort_keys=True)
        print('Backup successful to ' + filename)
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup the nhlpool database')
    parser.add_argument('root_psw', metavar='password',
                       help='The root password')
    parser.add_argument('-f','--filename', metavar='filename', default='<auto>', nargs='?',
                       help='The name of the file to backup to')
    parser.add_argument('-s', '--server', metavar='server', default='debug', nargs='?',
                       help='The server to use')

    args = parser.parse_args()

    if args.server == 'prod':
        print('Using production server')
        server = 'nhlpool.herokuapp.com/'
    else:
        print('Using debug server')
        server = 'localhost:5000'

    filename = args.filename
    if args.filename == '<auto>':
        print('Using auto filename')
        n=datetime.datetime.now()
        args.filename = 'backup-' +server + '-' + n.isoformat() + '.backup'

    backup(server, args.filename, args.root_psw)
