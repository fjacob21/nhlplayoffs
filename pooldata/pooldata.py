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
        if team_id not in yeardata.standings:
            standing = pooldatafactory.create_standing(team_id, pts, win, losses, ot, games_played, goals_against, goals_scored, ranks, extra_info)
            yeardata.standings[team_id] = standing
        return yeardata.standings[team_id]

    def add_matchup(self, year, id, round, home=0, away=0, start='', schedule={}, season_results={}, results=None):
        yeardata = self.add_year(year)
        if id not in yeardata.matchups:
            matchup = pooldatafactory.create_matchup(id, round, home, away, start, schedule, season_results, results)
            yeardata.matchups[id] = matchup
        return yeardata.matchups[id]

    def add_year(self, year):
        if year not in self.years:
            self.years[year] = PoolDataYear(year)
        return self.years[year]
