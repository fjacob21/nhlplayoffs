#!/usr/bin/python
import argparse
from datetime import datetime
from dateutil import tz
import json
import sys
import requests


class Updater(object):

    def __init__(self, server, year):
        self._server = server
        self._year = year
        self._current_round = 0
        self._teams = {}
        self._matchups = {}
        self.load()

    def run(self):
        if self._current_round == 0:
            self._teams = self.get_teams()
            self._matchups = self.create_matchups_tree()
            if len(list(self._teams.values())) > 0:
                standings = self.get_standings(list(self._teams.values()))
                self.create_matchups(standings)
            if self.is_season_finished():
                print('Playoff starting')
                self._current_round = 1
                self.store()
            else:
                print("Storing prelim results")
                self._current_round = 0
                self.store()
        else:
            self.update_matchups()
            self.store()

    def is_season_finished(self):
        for team in list(self._teams.values()):
            remaining = 82 - team['standings']['gamesPlayed']
            if remaining > 0:
                return False
        return True

    def create_matchups(self, standings):
        ealeader = standings['Eastern']['Atlantic'][0]
        emleader = standings['Eastern']['Metropolitan'][0]
        wcleader = standings['Western']['Central'][0]
        wpleader = standings['Western']['Pacific'][0]
        for team in standings['Eastern']['teams']:
            if int(team['standings']['wildCardRank']) == 1:
                e1wild = team
            if int(team['standings']['wildCardRank']) == 2:
                e2wild = team

        for team in standings['Western']['teams']:
            if int(team['standings']['wildCardRank']) == 1:
                w1wild = team
            if int(team['standings']['wildCardRank']) == 2:
                w2wild = team

        a1 = self._matchups['a1']
        m1 = self._matchups['m1']
        self.update_matchup(a1, ealeader['info']['id'])
        self.update_matchup(m1, emleader['info']['id'])
        if int(ealeader['standings']['conferenceRank']) < int(emleader['standings']['conferenceRank']):
            self.update_matchup(a1, e2wild['info']['id'])
            self.update_matchup(m1, e1wild['info']['id'])
        else:
            self.update_matchup(a1, e1wild['info']['id'])
            self.update_matchup(m1, e2wild['info']['id'])

        a2 = self._matchups['a2']
        self.update_matchup(a2, standings['Eastern']['Atlantic'][1]['info']['id'], standings['Eastern']['Atlantic'][2]['info']['id'])
        m2 = self._matchups['m2']
        self.update_matchup(m2, standings['Eastern']['Metropolitan'][1]['info']['id'], standings['Eastern']['Metropolitan'][2]['info']['id'])

        c1 = self._matchups['c1']
        p1 = self._matchups['p1']
        self.update_matchup(c1, wcleader['info']['id'])
        self.update_matchup(p1, wpleader['info']['id'])
        if int(wcleader['standings']['conferenceRank']) < int(wpleader['standings']['conferenceRank']):
            self.update_matchup(c1, w2wild['info']['id'])
            self.update_matchup(p1, w1wild['info']['id'])
        else:
            self.update_matchup(c1, w1wild['info']['id'])
            self.update_matchup(p1, w2wild['info']['id'])

        c2 = self._matchups['c2']
        self.update_matchup(c2, standings['Western']['Central'][1]['info']['id'], standings['Western']['Central'][2]['info']['id'])
        p2 = self._matchups['p2']
        self.update_matchup(p2, standings['Western']['Pacific'][1]['info']['id'], standings['Western']['Pacific'][2]['info']['id'])

    def set_matchup_childs(self, matchup, right, left):
        matchup['left'] = left
        matchup['right'] = right

    def create_matchup(self, id, round, next):
        matchup = {'id': id, 'home': 0, 'away': 0, 'round': round, 'start': '', 'result': {}, 'schedule': [], 'season': {}, 'next': next}
        matchup['left'] = None
        matchup['right'] = None
        matchup['result'] = {'home_win': 0, 'away_win': 0}
        return matchup

    def create_matchups_tree(self):
        matchups = {}
        sc = self.create_matchup('sc', 4, None)
        matchups[sc['id']] = sc

        e = self.create_matchup('e', 3, sc)
        w = self.create_matchup('w', 3, sc)
        matchups[e['id']] = e
        matchups[w['id']] = w

        a = self.create_matchup('a', 2, e)
        m = self.create_matchup('m', 2, e)
        c = self.create_matchup('c', 2, w)
        p = self.create_matchup('p', 2, w)
        matchups[a['id']] = a
        matchups[m['id']] = m
        matchups[c['id']] = c
        matchups[p['id']] = p

        a1 = self.create_matchup('a1', 1, a)
        a2 = self.create_matchup('a2', 1, a)
        m1 = self.create_matchup('m1', 1, m)
        m2 = self.create_matchup('m2', 1, m)
        c1 = self.create_matchup('c1', 1, c)
        c2 = self.create_matchup('c2', 1, c)
        p1 = self.create_matchup('p1', 1, p)
        p2 = self.create_matchup('p2', 1, p)
        matchups[a1['id']] = a1
        matchups[a2['id']] = a2
        matchups[m1['id']] = m1
        matchups[m2['id']] = m2
        matchups[c1['id']] = c1
        matchups[c2['id']] = c2
        matchups[p1['id']] = p1
        matchups[p2['id']] = p2

        # build tree
        self.set_matchup_childs(sc, e, w)

        self.set_matchup_childs(w, p, c)
        self.set_matchup_childs(e, m, a)

        self.set_matchup_childs(c, c2, c1)
        self.set_matchup_childs(p, p2, p1)
        self.set_matchup_childs(a, a2, a1)
        self.set_matchup_childs(m, m2, m1)

        return matchups

    def get_live_result(self, link):
        url = 'https://statsapi.web.nhl.com' + link
        live = requests.get(url).json()
        return live

    def get_team(self, id):
        url = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(id)
        team = requests.get(url).json()
        return team['teams'][0]

    def get_teams(self):
        ystr = str(self._year) + str(self._year + 1)
        url = 'https://statsapi.web.nhl.com/api/v1/standings?season=' + ystr
        standings = requests.get(url).json()
        teams = {}
        for record in standings["records"]:
            for team in record['teamRecords']:
                info = self.get_team(team['team']['id'])
                team_record = {'info': info, 'standings': team, 'schedule': []}
                teams[team['team']['id']] = team_record
        return teams

    def get_standings(self, teams):
        standings = {'Eastern': {'Atlantic': [], 'Metropolitan': [], 'teams': []},
                     'Western': {'Central': [], 'Pacific': [], 'teams': []},
                     'teams': []}

        league = sorted(teams, key=lambda k: int(k['standings']['divisionRank']))
        for team in league:
            standings['teams'].append(team)
            standings[team['info']['conference']['name']]['teams'].append(team)
            standings[team['info']['conference']['name']][team['info']['division']['name']].append(team)
        standings['teams'] = sorted(standings['teams'], key=lambda k: int(k['standings']['leagueRank']))

        standings['Eastern']['teams'] = sorted(standings['Eastern']['teams'], key=lambda k: int(k['standings']['conferenceRank']))
        standings['Western']['teams'] = sorted(standings['Western']['teams'], key=lambda k: int(k['standings']['conferenceRank']))

        standings['Eastern']['Atlantic'] = sorted(standings['Eastern']['Atlantic'], key=lambda k: int(k['standings']['divisionRank']))
        standings['Eastern']['Metropolitan'] = sorted(standings['Eastern']['Metropolitan'], key=lambda k: int(k['standings']['divisionRank']))
        standings['Western']['Central'] = sorted(standings['Western']['Central'], key=lambda k: int(k['standings']['divisionRank']))
        standings['Western']['Pacific'] = sorted(standings['Western']['Pacific'], key=lambda k: int(k['standings']['divisionRank']))

        return standings

    def parse_time(self, timestamp):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/New_York')
        utc = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        utc = utc.replace(tzinfo=from_zone)
        return utc.astimezone(to_zone)

    def get_matchup_schedule(self, matchup, schedules=None):
        home_id = matchup['home']
        away_id = matchup['away']
        result = []
        s = schedules
        if schedules is None:
            s = self.get_playoff_schedule(int(home_id))
        if 'dates' in s:
            for date in s['dates']:
                game = date['games'][0]
                game_home_id = game['teams']['home']['team']['id']
                game_away_id = game['teams']['away']['team']['id']
                if game['gameType'] == 'P':
                    if game_home_id == away_id or game_away_id == away_id:
                        result.append(game)
        else:
            print('No date in get matchup')
        result = sorted(result, key=lambda k: self.parse_time(k['gameDate']))
        return result

    def get_matchup_start(self, matchup):
        if len(matchup['schedule']) == 0:
            return ''
        return matchup['schedule'][0]['gameDate']

    def get_matchup_season_result(self, home, away):
        result = {'home_win': 0, 'away_win': 0, 'matchs': []}
        schedule = self._teams[home]['schedule']
        if len(schedule) == 0:
            schedule = self.get_schedule(home)
            # self._teams[home]['schedule'] = schedule

        if 'dates' in schedule:
            for date in schedule['dates']:
                game = date['games'][0]
                game_home_id = game['teams']['home']['team']['id']
                game_away_id = game['teams']['away']['team']['id']
                if game_home_id == away:
                    print(game['gameDate'], game['teams']['away']['score'], game['teams']['home']['score'])
                    if int(game['teams']['home']['score']) > int(game['teams']['away']['score']):
                        result['away_win'] = result['away_win'] + 1
                    elif int(game['teams']['home']['score']) < int(game['teams']['away']['score']):
                        result['home_win'] = result['home_win'] + 1
                    result['matchs'].append({'home': int(game['teams']['away']['score']), 'away': int(game['teams']['home']['score'])})
                if game_away_id == away:
                    print(game['gameDate'], game['teams']['home']['score'], game['teams']['away']['score'])
                    if int(game['teams']['home']['score']) > int(game['teams']['away']['score']):
                        result['home_win'] = result['home_win'] + 1
                    elif int(game['teams']['home']['score']) < int(game['teams']['away']['score']):
                        result['away_win'] = result['away_win'] + 1
                    result['matchs'].append({'home': int(game['teams']['home']['score']), 'away': int(game['teams']['away']['score'])})
        else:
            print('No date in get matchup season')
        return result

    def get_matchup_result(self, matchup):
        # statuscode = {}
        # statuscode[1] = 'Scheduled'
        # statuscode[2] = 'Pre-Game'
        # statuscode[3] = 'In Progress'
        # statuscode[4] = 'In Progress - Critical'
        # statuscode[5] = 'Game Over'
        # statuscode[6] = 'Final'
        # statuscode[7] = 'Final'

        result = {}
        # home_id = matchup['home']
        away_id = matchup['away']
        home_win = 0
        away_win = 0
        for game in matchup['schedule']:
            game_home_id = game['teams']['home']['team']['id']
            game_away_id = game['teams']['away']['team']['id']
            if game['gameType'] == 'P':
                if game_home_id == away_id or game_away_id == away_id:
                    if game_home_id == away_id:  # reverse
                        away_score = game['teams']['home']['score']
                        home_score = game['teams']['away']['score']
                        away_shots = game['linescore']['teams']['home']['shotsOnGoal']
                        home_shots = game['linescore']['teams']['away']['shotsOnGoal']
                    else:
                        away_score = game['teams']['away']['score']
                        home_score = game['teams']['home']['score']
                        away_shots = game['linescore']['teams']['away']['shotsOnGoal']
                        home_shots = game['linescore']['teams']['home']['shotsOnGoal']
                    if int(game['status']['statusCode']) == 7:
                        if home_score > away_score:
                            home_win = home_win + 1
                        elif home_score < away_score:
                            away_win = away_win + 1
                    elif int(game['status']['statusCode']) in [3, 4, 5, 6]:
                        hi = self._teams[matchup['home']]
                        ai = self._teams[matchup['away']]
                        # period = game['linescore']['currentPeriod']
                        result = self.get_live_result(game['link'])
                        if game_home_id == away_id:
                            away_stats = result['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']
                            home_stats = result['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']
                        else:
                            away_stats = result['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']
                            home_stats = result['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']

                        period = game['linescore']['currentPeriodOrdinal']
                        rtime = game['linescore']['currentPeriodTimeRemaining']
                        print("Game {status} \033[0;94m{h}\033[0m {hsc}-{asc} \033[0;94m{a}\033[0m - {t} of {p} - Shots:\033[0;94m{h}\033[0m {hsh}-{ash} \033[0;94m{a}\033[0m - Faceoff:\033[0;94m{h}\033[0m {hf}-{af} \033[0;94m{a}\033[0m".format(hf=home_stats['faceOffWinPercentage'], af=away_stats['faceOffWinPercentage'], status=game['status']['detailedState'], h=hi['info']['abbreviation'], hsc=home_score, asc=away_score, a=ai['info']['abbreviation'], p=period, t=rtime, hsh=home_shots, ash=away_shots))
        result['home_win'] = home_win
        result['away_win'] = away_win
        return result

    def is_matchup_finished(self, matchup):
        return matchup['result']['home_win'] == 4 or matchup['result']['away_win'] == 4

    def get_matchup_winner(self, matchup):
        if matchup['result']['home_win'] == 4:
            return matchup['home']
        if matchup['result']['away_win'] == 4:
            return matchup['away']
        return 0

    def update_matchup(self, matchup, home=0, away=0):
        if self.is_matchup_finished(matchup):
            return

        if matchup['home'] != 0 and matchup['away'] != 0:
            # update result and maybe pass to next stage
            matchup['schedule'] = self.get_matchup_schedule(matchup)
            if matchup['start'] == '':
                matchup['start'] = self.get_matchup_start(matchup)
            matchup['result'] = self.get_matchup_result(matchup)
            if self.is_matchup_finished(matchup) and matchup['next'] is not None:
                print('Finished', matchup['id'])
                self.update_matchup(matchup['next'], self.get_matchup_winner(matchup))
        else:
            if matchup['home'] == 0:
                matchup['home'] = home
                matchup['away'] = away
            else:
                matchup['away'] = home

            if matchup['home'] != 0 and matchup['away'] != 0:
                # Begin matchup
                hi = self._teams[matchup['home']]
                ai = self._teams[matchup['away']]
                if int(hi['standings']['leagueRank']) > int(ai['standings']['leagueRank']):
                    matchup['home'] = ai['info']['id']
                    matchup['away'] = hi['info']['id']
                hi = self._teams[matchup['home']]
                ai = self._teams[matchup['away']]
                matchup['season'] = self.get_matchup_season_result(matchup['home'], matchup['away'])
                matchup['schedule'] = self.get_matchup_schedule(matchup)
                matchup['start'] = self.get_matchup_start(matchup)

    def update_matchups(self):
        ms = list(self._matchups.values())
        ms = sorted(ms, key=lambda k: k['round'])
        for matchup in ms:
            self.update_matchup(matchup)

    def get_schedule(self, team):
        # print('Get schedule for ' + str(team))
        url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + str(self._year) + '-10-01&endDate=' + str(self._year + 1) + '-05-29&expand=schedule.teams,schedule.linescore,schedule.broadcasts,schedule.ticket,schedule.game.content.media.epg&leaderCategories=&site=en_nhlCA&teamId=' + str(team)
        team_schedule = requests.get(url)
        return team_schedule.json()

    def get_playoff_schedule(self, team):
        url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + str(self._year + 1) + '-04-01&endDate=' + str(self._year + 1) + '-06-15&expand=schedule.teams,schedule.linescore,&site=en_nhlCA&teamId=' + str(team)
        # print(url)
        team_schedule = requests.get(url)
        return team_schedule.json()

    def fetch_data(self):
        data = requests.get('http://' + self._server + '/nhlplayoffs/api/v3.0/' + str(self._year) + '/data').json()
        return data

    def update_data(self, data):
        url = 'http://' + self._server + '/nhlplayoffs/api/v3.0/' + str(self._year) + '/data'
        headers = {'content-type': 'application/json'}
        requests.post(url, data=json.dumps(data), headers=headers)

    def build_matchup_tree(self, raw_matchups):
        matchups = {}
        for matchup_raw in list(raw_matchups.values()):
            matchup = matchup_raw.copy()
            matchups[matchup['id']] = matchup

        for matchup in list(matchups.values()):
            next = matchup['next']
            right = matchup['right']
            left = matchup['left']
            if next in raw_matchups:
                matchup['next'] = matchups[next]
            if right in raw_matchups:
                matchup['right'] = matchups[right]
            if left in raw_matchups:
                matchup['left'] = matchups[left]
        return matchups

    def store_matchup_tree(self, matchups):
        raw_matchups = {}
        for matchup in list(matchups.values()):
            raw_matchup = matchup.copy()
            if matchup['next'] is not None:
                raw_matchup['next'] = matchup['next']['id']
            if matchup['right'] is not None:
                raw_matchup['right'] = matchup['right']['id']
            if matchup['left'] is not None:
                raw_matchup['left'] = matchup['left']['id']
            raw_matchups[raw_matchup['id']] = raw_matchup
        return raw_matchups

    def load(self):
        data = self.fetch_data()
        self._teams = {}
        for m in data['teams'].items():
            self._teams[int(m[0])] = m[1]
        self._current_round = data['current_round']
        self._matchups = self.build_matchup_tree(data['matchups'])

    def store(self):
        data = {}
        data['teams'] = self._teams
        data['current_round'] = self._current_round
        data['matchups'] = self.store_matchup_tree(self._matchups)
        self.update_data(data)

    def display(self):
        nb_round = 4
        width = (nb_round * 2) - 1
        heigh = (2**(nb_round - 1)) - 1
        display = [['' for x in range(width)] for y in range(heigh)]

        def walk_matchup_tree(root, x, y, dx):
            display[x][y] = root['id']
            if root['left'] is not None:
                walk_matchup_tree(root['left'], x + dx, y - (root['round'] - 1), dx)
            if root['right'] is not None:
                walk_matchup_tree(root['right'], x + dx, y + (root['round'] - 1), dx)

        display[3][2] = 'sc'
        walk_matchup_tree(self._matchups['w'], 2, 3, -1)
        walk_matchup_tree(self._matchups['e'], 4, 3, 1)

        for y in range(7):
            for x in range(7):
                id = display[x][y]
                if id != '':
                    matchup = self._matchups[id]
                    if matchup['home'] == 0:
                        sys.stdout.write('{0:15}'.format(id))
                    else:
                        home = self._teams[matchup['home']]['info']['abbreviation']
                        away = '?'
                        if matchup['away'] != 0:
                            away = self._teams[matchup['away']]['info']['abbreviation']
                        sys.stdout.write('\033[0;94m{0:3}\033[0m-{2} vs {3}-\033[0;94m{1:3}\033[0m'.format(home, away, matchup['result']['home_win'], matchup['result']['away_win']))
                else:
                    sys.stdout.write('{0:15}'.format(id))
            sys.stdout.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update the nhlpool database')
    parser.add_argument('-y', '--year', metavar='year', default='2018', nargs='?',
                        help='The year to work with')
    parser.add_argument('-s', '--server', metavar='server', default='debug', nargs='?',
                        help='The server to use')

    args = parser.parse_args()

    if args.server == 'prod':
        print('Using production server')
        server = 'nhlpool.herokuapp.com/'
    else:
        print('Using debug server')
        server = 'localhost:5000'

    upd = Updater(server, int(args.year))
    upd.run()
    upd.display()
