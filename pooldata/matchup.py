from powerdict import PowerDict


class Matchup(PowerDict):

    def __init__(self, id, round, home=0, away=0, start='', schedule={}, season_results={}, results=None):
        matchup = {}
        matchup['id'] = id
        matchup['home'] = home
        matchup['away'] = away
        matchup['round'] = round
        matchup['start'] = start
        matchup['schedule'] = schedule
        matchup['season_results'] = season_results
        matchup['results'] = results
        self._data = matchup

    @property
    def started(self):
        return False
