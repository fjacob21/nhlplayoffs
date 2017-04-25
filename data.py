from datetime import datetime
from dateutil import tz
import postgres_store


class Data():

    def __init__(self, player_id=None):
        self.to_zone = tz.gettz('America/New_York')
        self.from_zone = tz.gettz('UTC')
        self._rawData = self.RawData()
        years = self._rawData.get_years()
        self._players = self._rawData.get_players()
        self._matchups = {}
        self._matchups_list = {}
        self._predictions = {}
        self._winners = {}
        self._teams = {}
        for year in years:
            self._teams[year] = self._rawData.get_teams(year)
            self._matchups[year] = self._rawData.get_matchups(year)
            self._matchups_list[year] = list(self._matchups[year].values())
            self._predictions[year] = self._rawData.get_predictions(year)
            self._winners[year] = self._rawData.get_winners(year)
        self.build_players(player_id)

    def add_player_team(self, team, round, teams, rounds_teams):
        if team not in teams:
            teams[team] = 1
        else:
            teams[team] = teams[team] + 1
        if team not in rounds_teams[round]:
            rounds_teams[round][team] = 1
        else:
            rounds_teams[round][team] = rounds_teams[round][team] + 1

    def add_player_games(self, games, round, total_games, rounds_games):
        if games != 0:
            if games not in total_games:
                total_games[games] = 1
            else:
                total_games[games] = total_games[games] + 1
            if games not in rounds_games[round]:
                rounds_games[round][games] = 1
            else:
                rounds_games[round][games] = rounds_games[round][games] + 1

    def matchup_result(self, matchup):
        winner = 0
        games = 0
        if matchup['result']['home_win'] == 4:
            winner = matchup['home']
            games = matchup['result']['home_win'] + matchup['result']['away_win']
        if matchup['result']['away_win'] == 4:
            winner = matchup['away']
            games = matchup['result']['home_win'] + matchup['result']['away_win']
        return winner, games

    def build_player_matchup_result(self, year, pred, winner, games, result):
        if pred['winner'] == winner:
            result['has_winner'] = True
            result['winner_rank'] = self._teams[year][winner]['standings']['conferenceRank']
            if pred['games'] == games:
                result['has_games'] = True

    def build_players(self, player_id=None):
        for p in self._players:
            p['predictions'] = {}

            prediction_count = 0
            prediction_teams = {}
            rounds_teams = {1: {}, 2: {}, 3: {}, 4: {}}
            total_games = {}
            rounds_games = {1: {}, 2: {}, 3: {}, 4: {}}
            missings_predictions = []
            now = self.now()

            for y in self._matchups_list:
                p['predictions'][y] = []
                for m in self._matchups_list[y]:
                    if not player_id or player_id == p['id'] or self.is_matchup_started(m, now):
                        pred = self.find_prediction(p['id'], y, m['round'], m['home'], m['away'])
                        result = {'has_winner': False, 'has_games': False, 'winner_rank': 0}
                        if pred and pred['winner'] != 0:
                            prediction_count = prediction_count + 1
                            self.add_player_team(pred['winner'], pred['round'], prediction_teams, rounds_teams)
                            self.add_player_games(pred['games'], pred['round'], total_games, rounds_games)

                            winner, games = self.matchup_result(m)
                            self.build_player_matchup_result(y, pred, winner, games, result)

                            if 'player' in pred:
                                del pred['player']
                        elif m['home'] != 0 and m['away'] != 0:
                            missings_predictions.append(m)

                        if 'schedule' in m:
                            del m['schedule']
                        if 'season' in m:
                            del m['season']
                        m['year'] = y
                        p['predictions'][y].append({'matchup': m, 'prediction': pred, 'result': result})

            p['prediction_count'] = prediction_count
            favorite_team = 0
            if len(prediction_teams) > 0:
                favorite_team = max(prediction_teams, key=prediction_teams.get)
            p['favorite_team'] = favorite_team
            p['games_stats'] = {'total': total_games, 'rounds': rounds_games}
            p['missings'] = missings_predictions
        # pprint(self._players)

    def parse_time(self, timestamp):
        utc = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        utc = utc.replace(tzinfo=self.from_zone)
        return utc.astimezone(self.to_zone)

    def get_start(self, matchup):
        if 'start' in matchup and matchup['start']:
            return self.parse_time(matchup['start'])
        return None

    def now(self):
        return datetime.now(tz.tzlocal()).astimezone(self.to_zone)

    def is_round_started(self, year, round, now=None):
        if not now:
            now = self.now()

        for matchup in self._matchups_list[year]:
            if matchup['round'] == round and self.is_matchup_started(matchup, now):
                return True
        return False

    def is_matchup_started(self, matchup, now=None):
        if not now:
            now = self.now()
        start = self.get_start(matchup)
        if start is not None:
            if now > start:
                return True
        return False

    def get_players(self):
        return self._players

    def find_prediction(self, player_id, year, round, home, away):
        result = None
        for p in self._predictions[year]:
            if p['player'] == player_id and p['round'] == round and p['home'] == home and p['away'] == away:
                return p.copy()
        return result

    def find_winner(self, player_id, year):
        for w in self._winners[year]:
            if w['player'] == player_id:
                return w['winner']
        print('not Found', player_id, year)
        return 0

    def calculate_result_pts(self, result):
        pts = 0
        if result['has_winner']:
            pts = pts + 10
            pts = pts + int(result['winner_rank'])
            if result['has_games']:
                pts = pts + 5
        return pts

    def get_results(self, player_id, year):
        results = []
        now = self.now()
        for player in self._players:
            if player['prediction_count'] > 0:
                pts = 0
                oldpts = 0
                winner = 0
                if not player_id or player_id == player['id'] or self.is_round_started(year, 1, now):
                    winner = self.find_winner(player['id'], year)
                player_preds = []
                for pred in player['predictions'][year]:
                    if pred['prediction']:
                        player_preds.append(pred['prediction'])
                    pts = pts + self.calculate_result_pts(pred['result'])
                victories = {'winner_count': 0, 'games_count': 0}
                results.append({'player': player['name'], 'pts': pts, 'oldpts': oldpts, 'winner': winner, 'predictions': player_preds, 'victories': victories})
        return results

    class RawData():
        def __init__(self):
            _db = postgres_store.get_default()
            self._data = _db.backup()

        def get_years(self):
            return self._data['datav2'].keys()

        def get_players(self):
            players = self._data['players'][1]
            l = list(players.items())
            result = []
            for player in l:
                p = player[1].copy()
                del p['psw']
                p['id'] = player[0]
                result.append(p)
            return result

        def get_teams(self, year):
            dbteams = self._data['datav2'][year]['teams']
            teams = {}
            for m in dbteams.items():
                teams[int(m[0])] = m[1]
            return teams

        def get_matchups(self, year):
            return self._data['datav2'][year]['matchups']

        def get_predictions(self, year):
            return self._data['predictions'][year]['matchups']

        def get_winners(self, year):
            return self._data['predictions'][year]['winners']
