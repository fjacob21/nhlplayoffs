#!/usr/bin/env python3
import argparse
import json
import requests


def restore(server, filename, root_psw):
    try:
        with open(filename, 'r') as infile:
            data = json.load(infile)

        url = 'http://' + server + '/nhlplayoffs/api/v2.0/restore'
        headers = {'content-type': 'application/json'}
        data = {'root_psw': root_psw, 'data': data}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if not r.ok:
            print('Invalid request!!!!')
            return False

        if r.json()['result']:
            print('Restore successful')
            return True
        else:
            print('Invalid parameter')
            return False
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Restore an nhlpool database backup')
    parser.add_argument('root_psw', metavar='password',
                        help='The root password')
    parser.add_argument('filename', metavar='filename',
                        help='The name of the file to restore')
    parser.add_argument('-s', '--server', metavar='server', default='debug', nargs='?',
                        help='The server to use')

    args = parser.parse_args()

    if args.server == 'prod':
        print('Using production server')
        server = 'nhlpool.roblab.net/'
    else:
        print('Using debug server')
        server = 'localhost:5000'

    var = input("Are you sure you want to errase all data on {server} and replace it with backup {backup}? ".format(server=server, backup=args.filename))
    if var == 'y':
        restore(server, args.filename, args.root_psw)
