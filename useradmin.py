#!/usr/bin/env python3
import argparse
from datetime import datetime
from dateutil import tz
import json
import requests


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
        url = 'http://' + server + '/nhlplayoffs/api/v2.0/players/' + user
        headers = {'content-type': 'application/json'}
        data = {'root_psw': root_psw}
        r = requests.delete(url, data=json.dumps(data), headers=headers)
        if not r.ok:
            print('Invalid request!!!!')
            return False
        if r.json()['result']:
            print('Remove {0} successful'.format(user))
            return True
        else:
            print('Invalid parameter')
            return False
    except Exception as e:
        print(e)
        return False


def remove_inactive_users(server, root_psw):
    _, _, inactives,_ = getusers(server)
    for player in inactives:
        user = player['name']
        var = input("Are you sure you want to errase user: {user} on {server}? ".format(server=server, user=user))
        if var == 'y':
            removeuser(server, user, root_psw)


def getusers(server):
    users = []
    actives = []
    inactives = []
    missings = []
    try:
        url = 'http://' + server + '/nhlplayoffs/api/v2.0/players'
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        if not r.ok:
            print('Invalid request!!!!')
            return []
        users = r.json()['players']
        inactives = [p for p in users if p['prediction_count'] == 0]
        for user in users:
            if user['prediction_count'] != 0:
                actives.append(user)
                for m in user['missings']:
                    if m['start'] and now() < parse_time(m['start']):
                        missings.append(user)
                        break
    except Exception as e:
        print(e)
    return users, actives, inactives, missings


def parse_time(timestamp):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)


def now():
    to_zone = tz.gettz('America/New_York')
    return datetime.now(tz.tzlocal()).astimezone(to_zone)


def list_inactive_users(server):
    print("list inactive users")
    teams = getteams(server)
    _, _, inactive, _  = getusers(server)
    print_users(inactive, teams)

def list_users(server):
    print("list users")
    teams = getteams(server)
    users, _, _, _  = getusers(server)
    print_users(users, teams)

def list_active_users(server):
    print("list active users")
    teams = getteams(server)
    _, actives, _, _  = getusers(server)
    print_users(actives, teams)

def print_active_users_email(server):
    print("print active users email")
    _, users, _, _  = getusers(server)
    email_list = ""
    for player in users:
        print(f"\033[0;94m{player['name']}\033[0m : {player['email']}")
        email_list += f"{player['email']}; "
    print(email_list[:-2])

def list_missing_users(server):
    print("list missing users")
    teams = getteams(server)
    _, _, _, missings  = getusers(server)
    print_users(missings, teams, True)


def print_users(users, teams, show_missing=False):
    for player in users:
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
                    mean = (float(player['games_stats']['total'][game]) / float(player['prediction_count']) * 100)
                print("\t\t\033[1;30m{g}:\033[0m {n:3.2f}%".format(g=game, n=mean))
        if player['missings'] and len(player['missings']) > 0:
            print("\t\033[1;30mMissings:\033[0m ")
            for missing in player['missings']:
                if show_missing and missing['start'] and now() < parse_time(missing['start']):
                    print("\t\tYear:{y} Round:{r} Home:{h} Away:{a} Start:{s}".format(y=missing['year'], r=missing['round'], h=missing['home'], a=missing['away'], s=missing['start']))
        print("\t\033[1;30mTeam result stats:\033[0m ")
        team_results = sorted(player['team_results'].items(), key=lambda x: -x[1])
        for t in team_results:
            team = teams[int(t[0])]
            team = team['info']['abbreviation']
            result = t[1]
            print("\t\t\033[1;30m{t}:\033[0m {r:3.2f}%".format(t=team, r=result))
        print("\t\033[1;30mGames result stats:\033[0m ")
        games_results = sorted(player['games_results'].items(), key=lambda x: -x[1])
        for t in games_results:
            print("\t\t\033[1;30m{g}:\033[0m {r:3.2f}%".format(g=t[0], r=t[1]))


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
        server = 'nhlpool.roblab.net/'
    else:
        print('Using debug server')
        server = 'localhost:5000'

    cmd = args.cmd
    user = args.user
    root_psw = args.root_psw
    if cmd == 'list':
        list_users(server)
    elif cmd == 'listinactive':
        list_inactive_users(server)
    elif cmd == 'listactive':
        list_active_users(server)
    elif cmd == 'printemail':
        print_active_users_email(server)
    elif cmd == 'listmissing':
        list_missing_users(server)
    elif cmd == 'remove':
        removeuser(server, user, root_psw)
    elif cmd == 'removeinactive':
        remove_inactive_users(server, root_psw)
    else:
        print('Invalid command!!!')
