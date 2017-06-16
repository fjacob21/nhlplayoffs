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


class PoolData(object):
    def __init__(self):
        self._teams = {}
        self._players = []
        self._years = {}

    def add_team(self, id, abbreviation, name, fullname, city, active=False, creation_year=0, website='', venue=None, league_info=None):
        if id not in self._teams:
            team = pooldatafactory.create_team(id, abbreviation, name, fullname, city, active, creation_year, website, venue, league_info)
            self._teams[id] = team
        return self._teams[id]

    def add_standings(self, year, team_id, pts, win, losses, ot, games_played, goals_against, goals_scored, ranks, extra_info={}):
        yeardata = self.add_year(year)
        if team_id not in yeardata.standings:
            standing = pooldatafactory.create_standings(team_id, pts, win, losses, ot, games_played, goals_against, goals_scored, ranks, extra_info)
            yeardata.standings[team_id] = standing
        return yeardata.standings[team_id]

    def add_matchup(self, year, id, round, home=0, away=0, start='', schedule={}, season_results={}, results=None):
        yeardata = self.add_year(year)
        if id not in yeardata.matchups:
            matchup = pooldatafactory.create_matchup(id, round, home, away, start, schedule, season_results, results)
            yeardata.matchups[id] = matchup
        return yeardata.matchups[id]

    def add_year(self, year):
        if year not in self._years:
            self._years[year] = PoolDataYear(year)
        return self._years[year]
