from game import GAME_STATE_SCHEDULED, GAME_STATE_FINISHED
import pooldatafactory
from powerdict import PowerDict


class MatchupResult(PowerDict):

    def __init__(self, home_win=0, away_win=0, games=[]):
        results = {}
        results['home_win'] = home_win
        results['away_win'] = away_win
        results['games'] = games
        self._data = results

    def add_game(self, home, away, date='', state=GAME_STATE_SCHEDULED, home_goal=0, away_goal=0, extra_data=None):
        game = pooldatafactory.create_matchup_game(home, away, date, state, home_goal, away_goal, extra_data)
        self.games.append(game)
        if state == GAME_STATE_FINISHED:
            if home_goal > away_goal:
                self.home_win = self.home_win + 1
            else:
                self.away_win = self.away_win + 1
