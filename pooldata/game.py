from powerdict import PowerDict

GAME_STATE_SCHEDULED = 1
GAME_STATE_IN_PROGRESS = 2
GAME_STATE_FINISHED = 3


class Game(PowerDict):

    def __init__(self, home, away, date='', state=GAME_STATE_SCHEDULED, home_goal=0, away_goal=0, extra_data=None):
        game = {}
        game['home'] = home
        game['away'] = away
        game['date'] = date
        game['state'] = state
        game['home_goal'] = home_goal
        game['away_goal'] = away_goal
        game['extra_data'] = extra_data
        self._data = game
