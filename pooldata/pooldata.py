import pooldatafactory
from powerdict import PowerDict
from matchuptree import MatchupTree


class PoolDataYear(PowerDict):

    def __init__(self, year=0):
        yeardata = {}
        yeardata['year'] = year
        yeardata['matchups'] = MatchupTree()
        yeardata['standings'] = {}
        yeardata['predictions'] = []
        yeardata['winners'] = {}
        self._data = yeardata

    def add_standing(self, team_id, pts, win, losses, ot, games_played, goals_against, goals_scored, ranks, extra_info={}):
        if team_id not in self.standings:
            standing = pooldatafactory.create_standing(team_id, pts, win, losses, ot, games_played, goals_against, goals_scored, ranks, extra_info)
            self.standings[team_id] = standing
        return self.standings[team_id]

    def add_matchup(self, id, round, home=0, away=0, start='', playoff=None, season=None):
        if id not in self.matchups:
            matchup = pooldatafactory.create_matchup(id, round, home, away, start, playoff, season)
            self.matchups.create_node(id, round, matchup=matchup)
        return self.matchups[id].matchup


class PoolData(PowerDict):
    def __init__(self):
        self._data = {}
        self.teams = {}
        self.players = []
        self.years = {}

    def add_team(self, id, abbreviation, name, fullname, city, active=False, creation_year=0, website='', venue=None, league_info=None):
        if id not in self.teams:
            team = pooldatafactory.create_team(id, abbreviation, name, fullname, city, active, creation_year, website, venue, league_info)
            self.teams[id] = team
        return self.teams[id]

    def add_standing(self, year, team_id, pts, win, losses, ot, games_played, goals_against, goals_scored, ranks, extra_info={}):
        yeardata = self.add_year(year)
        return yeardata.add_standing(team_id, pts, win, losses, ot, games_played, goals_against, goals_scored, ranks, extra_info)

    def add_matchup(self, year, id, round, home=0, away=0, start='', playoff=None, season=None):
        yeardata = self.add_year(year)
        return yeardata.add_matchup(id, round, home, away, start, playoff, season)

    def add_year(self, year):
        if year not in self.years:
            self.years[year] = PoolDataYear(year)
        return self.years[year]
