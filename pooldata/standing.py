from powerdict import PowerDict


class Standing(PowerDict):

    def __init__(self, team_id=0, pts=0, win=0, losses=0, ot=0, games_played=0, goals_against=0, goals_scored=0, ranks=0, extra_info={}):
        standing = {}
        standing['team_id'] = team_id
        standing['pts'] = pts
        standing['win'] = win
        standing['losses'] = losses
        standing['ot'] = ot
        standing['games_played'] = games_played
        standing['goals_against'] = goals_against
        standing['goals_scored'] = goals_scored
        standing['ranks'] = ranks
        standing['extra_info'] = extra_info
        self._data = standing
