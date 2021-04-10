class MatchupTree(object):

    def __init__(self):
        self._matchups = {}

    def get(self, matchup_id):
        return self._matchups.get(matchup_id, [])
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self._matchups[key] = value
    
    def __iter__(self):
        return self._matchups.__iter__()
    
    def __contains__(self, key):
        return key in self._matchups

    def __len__(self):
        return len(self.matchups)

    @property
    def matchups(self):
        return list(self._matchups.values())

    def restore(self, raw_matchups):
        matchups = {}
        for matchup_raw in list(raw_matchups.values()):
            matchup = matchup_raw.copy()
            matchups[matchup['id']] = matchup

        for matchup in list(matchups.values()):
            next = matchup['next']
            right = matchup['right']
            left = matchup['left']
            if next in raw_matchups:
                matchup['next'] = matchups[next]
            if right in raw_matchups:
                matchup['right'] = matchups[right]
            if left in raw_matchups:
                matchup['left'] = matchups[left]
        return matchups

    def store(self):
        raw_matchups = {}
        for matchup in list(self._matchups.values()):
            raw_matchup = matchup.copy()
            if matchup['next'] is not None:
                raw_matchup['next'] = matchup['next']['id']
            if matchup['right'] is not None:
                raw_matchup['right'] = matchup['right']['id']
            if matchup['left'] is not None:
                raw_matchup['left'] = matchup['left']['id']
            raw_matchups[raw_matchup['id']] = raw_matchup
        return raw_matchups
    
    def set_matchup_childs(self, matchup, right, left):
        matchup['left'] = left
        matchup['right'] = right

    def create_matchup(self, id, round, next):
        matchup = {'id': id, 'home': 0, 'away': 0, 'round': round, 'start': '', 'result': {}, 'schedule': [], 'season': {}, 'next': next}
        matchup['left'] = None
        matchup['right'] = None
        matchup['result'] = {'home_win': 0, 'away_win': 0}
        return matchup
    
    def is_matchup_finished(self, matchup, victory=4):
        return matchup['result']['home_win'] == victory or matchup['result']['away_win'] == victory

    def get_matchup_winner(self, matchup, victory=4):
        if matchup['result']['home_win'] == victory:
            return matchup['home']
        if matchup['result']['away_win'] == victory:
            return matchup['away']
        return 0

    def get_matchup_round(self, round):
        matchups = []
        for matchup in self._matchups.values():
            if matchup['round'] == round:
                matchups.append(matchup)
        return matchups
    
    def get_matchup_start(self, matchup):
        if len(matchup['schedule']) == 0:
            return ''
        return matchup['schedule'][0]['gameDate']