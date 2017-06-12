from powerdict import PowerDict


class MatchupResult(PowerDict):

    def __init__(self, home_win=0, away_win=0):
        results = {}
        results['home_win'] = home_win
        results['away_win'] = away_win
        self._data = results
