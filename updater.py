from datetime import datetime
from dateutil import tz
import json
import sys
import requests
from nhlquery import NHLQuery
from matchuptree import MatchupTree

class Updater(object):

    def __init__(self, server, year):
        self._server = server
        self._year = year
        self._season_games = 82
        self._current_round = 0
        self._auto_move = False
        self._teams = {}
        self._standings = {}
        self._query = NHLQuery(self._year)
        self._matchups = MatchupTree()
        self.load()
    
    @property
    def teams(self):
        return list(self._teams.values())

    def load(self):
        data = self.fetch_data()
        self._teams = {}
        for m in data['teams'].items():
            self._teams[m[0]] = m[1]
        self._current_round = data['current_round']
        self._matchups.restore(data['matchups'])

    def store(self):
        data = {}
        data['teams'] = self._teams
        data['current_round'] = self._current_round
        data['matchups'] = self._matchups.store()
        self.update_data(data)

    def fetch_data(self):
        data = requests.get('http://' + self._server + '/nhlplayoffs/api/v3.0/' + str(self._year) + '/data').json()
        return data

    def update_data(self, data):
        url = 'http://' + self._server + '/nhlplayoffs/api/v3.0/' + str(self._year) + '/data'
        headers = {'content-type': 'application/json'}
        requests.post(url, data=json.dumps(data), headers=headers)
    
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
        walk_matchup_tree(self._matchups['sc1'], 2, 3, -1)
        walk_matchup_tree(self._matchups['sc2'], 4, 3, 1)

        for y in range(7):
            for x in range(7):
                id = display[x][y]
                if id != '':
                    matchup = self._matchups[id]
                    start = ""
                    if matchup["start"]:
                        start = "*"
                    if matchup['home'] == 0:
                        sys.stdout.write('{0:15}'.format(id))
                    else:
                        home = self._teams[matchup['home']]['info']['abbreviation']
                        away = '?'
                        if matchup['away'] != 0:
                            away = self._teams[matchup['away']]['info']['abbreviation']
                        sys.stdout.write('\033[0;94m{0:3}\033[0m-{2} vs {3}-\033[0;94m{1:3}{4}\033[0m'.format(home, away, matchup['result']['home_win'], matchup['result']['away_win'], start))
                else:
                    sys.stdout.write('{0:15}'.format(id))
            sys.stdout.write('\n')
        
        league = self.get_league_standing()
        print("\nLeague standing")
        print(f"Tea gp wi lo ot pts")
        print("-------------------")
        for team in league:
            print(f"\033[0;94m{team['info']['abbreviation']}\033[0m {team['standings']['gamesPlayed']:2} {team['standings']['leagueRecord']['wins']:2} {team['standings']['leagueRecord']['losses']:2} {team['standings']['leagueRecord']['ot']:2} {team['standings']['points']:3}")

    
    def is_season_finished(self):
        for team in self.teams:
            remaining = self._season_games - team['standings']['gamesPlayed']
            if remaining > 0:
                return False
        return True
    
    def is_all_matchup_have_start(self, round):
        matchups = self._matchups.get_matchup_round(round)
        for matchup in matchups:
            if matchup['start'] == '':
                return False
        return True

    def is_round_finished(self, round):
        matchups = self._matchups.get_matchup_round(round)
        for matchup in matchups:
            if not self._matchups.is_matchup_finished(matchup):
                return False
        return True

    def get_league_standing(self):
        return sorted(list(self._teams.values()), key=lambda k: int(k['standings']['leagueRank']))

    def get_season_standings(self):
        return self.get_standings(self.teams)
    
    def get_round_standings(self, round):
        teams = []
        matchups = self._matchups.get_matchup_round(1)
        for matchup in matchups:
            teams.append(self._teams[matchup['home']])
            teams.append(self._teams[matchup['away']])
        return self.get_standings(teams)

    def get_round_winners_standings(self, round):
        teams = []
        matchups = self._matchups.get_matchup_round(round)
        for matchup in matchups:
            winner = self._matchups.get_matchup_winner(matchup)
            if winner:
                teams.append(self._teams[winner])
        return self.get_standings(teams)

    def get_matchup_schedule(self, matchup, schedules=None):
        home_id = matchup['home']
        away_id = matchup['away']
        result = []
        s = schedules
        if schedules is None:
            s = self._query.get_playoff_schedule(home_id)
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

    def parse_time(self, timestamp):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/New_York')
        utc = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        utc = utc.replace(tzinfo=from_zone)
        return utc.astimezone(to_zone)

    def update_round_home(self, winner, rnext):
        for r in rnext:
            if r[1]:
                if r[0]["home"] == 0:
                    print("Set Matchup home", r[0]['id'], r[0]['home'], r[0]['away'], winner)
                    self.update_matchup(r[0], winner)
                    return
            else:
                if r[0]["away"] == 0:
                    print("Set Matchup away", r[0]['id'], r[0]['home'], r[0]['away'], winner)
                    self.update_matchup(r[0], winner)
                    return

    def update_round_away(self, winner, rnext):
        rnr = rnext.copy()
        rnr.reverse()
        for r in rnr:
            if r[1]:
                if r[0]["home"] == 0:
                    print("Set Matchup home", r[0]['id'], r[0]['home'], r[0]['away'], winner)
                    self.update_matchup(r[0], winner)
                    return
            else:
                if r[0]["away"] == 0:
                    print("Set Matchup away", r[0]['id'], r[0]['home'], r[0]['away'], winner)
                    self.update_matchup(r[0], winner)
                    return

    

    def get_matchup_season_result(self, home, away):
        result = {'home_win': 0, 'away_win': 0, 'matchs': []}
        schedule = self._teams[home]['schedule']
        if len(schedule) == 0:
            schedule = self._query.get_schedule(home)
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
                    away_shots = 0
                    home_shots = 0
                    if game_home_id == away_id:  # reverse
                        away_score = game['teams']['home']['score']
                        home_score = game['teams']['away']['score']
                        if 'linescore' in game:
                            away_shots = game['linescore']['teams']['home']['shotsOnGoal']
                            home_shots = game['linescore']['teams']['away']['shotsOnGoal']
                    else:
                        away_score = game['teams']['away']['score']
                        home_score = game['teams']['home']['score']
                        if 'linescore' in game:
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
                        result = self._query.get_live_result(game['link'])
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

    def update_matchups(self):
        ms = self._matchups.matchups
        ms = sorted(ms, key=lambda k: k['round'])
        for matchup in ms:
            self.update_matchup(matchup)

    def update_matchup(self, matchup, home=0, away=0):
        if self._matchups.is_matchup_finished(matchup):
            return

        if matchup['home'] != 0 and matchup['away'] != 0:
            # update result and maybe pass to next stage
            matchup['schedule'] = self.get_matchup_schedule(matchup)
            if matchup['start'] == '':
                matchup['start'] = self._matchups.get_matchup_start(matchup)
            matchup['result'] = self.get_matchup_result(matchup)
            if self._auto_move:
                if self.is_matchup_finished(matchup) and matchup['next'] is not None:
                    print('Finished', matchup['id'])
                    self.update_matchup(matchup['next'], self.get_matchup_winner(matchup))
        else:
            if matchup['home'] == 0:
                matchup['home'] = home
                matchup['away'] = away
            else:
                matchup['away'] = home
            print(self._teams)
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
                matchup['start'] = self._matchups.get_matchup_start(matchup)
                matchup['result'] = self.get_matchup_result(matchup)

    def create_matchups(self, standings, round):
        if round == 0:
            self.create_matchups_round0(standings)
        elif round == 1:
            self.create_matchups_round1(standings)
        elif round == 2:
            self.create_matchups_round2(standings)
        elif round == 3:
            self.create_matchups_round3(standings)

    def create_matchups_round0(self, standings):
        pass

    def create_matchups_round1(self, standings):
        pass

    def create_matchups_round2(self, standings):
        pass

    def create_matchups_round3(self, standings):
        pass
    
    def run(self):
        pass

    def create_matchups_tree(self):
        pass
    
    def get_standings(self, teams):
        pass

    