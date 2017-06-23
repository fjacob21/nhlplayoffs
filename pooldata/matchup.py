from matchupresult import MatchupResult
from powerdict import PowerDict


class Matchup(PowerDict):

    def __init__(self, id=0, round=0, home=0, away=0, start='', playoff=MatchupResult(), season=MatchupResult()):
        matchup = {}
        matchup['id'] = id
        matchup['home'] = home
        matchup['away'] = away
        matchup['round'] = round
        matchup['start'] = start
        matchup['playoff'] = playoff
        matchup['season'] = season
        self._data = matchup

    @property
    def started(self):
        return False
