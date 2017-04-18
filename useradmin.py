#!/usr/bin/python
import argparse
import datetime
import json
import sys
import requests
from pprint import pprint

def getteams(server):
    try:
        url = 'http://' + server + '/nhlplayoffs/api/v2.0/teams'
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        if not r.ok:
            print('Invalid request!!!!')
            return {}
        rteams = r.json()['teams']
        teams = {}
        for t in rteams:
            teams[int(t)] = rteams[t]
        return teams

    except Exception as e:
        print(e)
        return {}

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

def remove_inactive_users(server, root_psw):
    players = getusers(server, True)
    for player in players:
        user = player['name']
        var = raw_input("Are you sure you want to errase user: {user} on {server}? ".format(server=server,user=user))
        if var == 'y':
            removeuser(server, user, root_psw)

def getusers(server, inactive=False, missing=False):
    try:
        url = 'http://' + server + '/nhlplayoffs/api/v2.0/players'
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        if not r.ok:
            print('Invalid request!!!!')
            return []
        players = r.json()['players']
        players = [p for p in players if p['prediction_count'] == 0 or not inactive ]
        if missing:
            ps = []
            for p in players:
                if p['prediction_count'] != 0:
                    for m in p['missings']:
                        print(p['name'], m, p['missings'][m])
                        if len(p['missings'][m]):
                            ps.append(p)
                            break
            players = ps
        return players

    except Exception as e:
        print(e)
        return []

def listusers(server, inactive=False, missing=False):
    teams = getteams(server)
    players = getusers(server, inactive, missing)
    for player in players:
        print("\033[0;94m{n}\033[0m".format(n=player['name']))
        if 'last_login' in player:
            print("\t\033[1;30mLast Login:\033[0m {l}".format(l=player['last_login']))
        print("\t\033[1;30mEmail:\033[0m {e}".format(e=player['email']))
        print("\t\033[1;30mPredictions:\033[0m {p}".format(p=player['prediction_count']))
        if player['favorite_team'] > 0 and player['favorite_team'] in teams:
            team = teams[player['favorite_team']]
            team = team['info']['abbreviation']
            print("\t\033[1;30mFav team:\033[0m {t}".format(t=team))
        if len(player['games_stats']['total']) > 0:
            print("\t\033[1;30mGames prediction stats:\033[0m ")
            for game in player['games_stats']['total']:
                mean = 0
                if int(player['prediction_count']) != 0:
                    mean = (float(player['games_stats']['total'][game])/float(player['prediction_count'])*100)
                print("\t\t\033[1;30m{g}:\033[0m {n:3.2f}%".format(g=game, n=mean))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage the nhlpool players')
    parser.add_argument('cmd', metavar='cmd',
                       help='The command to execute')
    parser.add_argument('root_psw', metavar='password', default='', nargs='?',
                       help='The root password')
    parser.add_argument('user', metavar='user', default='', nargs='?',
                       help='The user')
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
    elif cmd == 'listinactive':
        listusers(server, True)
    elif cmd == 'listmissing':
        listusers(server, False, True)
    elif cmd == 'remove':
        removeuser(server, user, root_psw)
    elif cmd == 'removeinactive':
        remove_inactive_users(server, root_psw)
    else:
        print('Invalid command!!!')