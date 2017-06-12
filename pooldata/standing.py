from powerdict import PowerDict


class Standing(PowerDict):

    def __init__(self, team_id, pts, win, losses, ot, games_played, goals_against, goals_scored, ranks, extra_info={}):
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
