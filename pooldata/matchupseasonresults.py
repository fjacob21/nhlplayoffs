from powerdict import PowerDict


class MatchupSeasonResults(PowerDict):

    def __init__(self, home_win=0, away_win=0, games=[]):
        results = {}
        results['home_win'] = home_win
        results['away_win'] = away_win
        results['games'] = games
        self._data = results
