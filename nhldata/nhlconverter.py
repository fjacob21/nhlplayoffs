class NHLDataConverter(object):

    def __init__(self, nhl_data, pool_data):
        self._nhl_data = nhl_data
        self._pool_data = pool_data

    def extract_team_info(self, team):
        info = {}
        info['abbreviation'] = team['abbreviation']
        info['name'] = team['teamName']
        info['active'] = team['active']
        info['city'] = team['locationName']
        info['fullname'] = team['name']
        info['creation_year'] = team['firstYearOfPlay']
        info['website'] = team['officialSiteUrl']
        return info

    def extract_team_venue(self, team):
        venue_city = team['venue']['city']
        venue_name = team['venue']['name']
        # venue_timezone = team['venue']['timeZone']['id']
        return self._pool_data.create_team_venue(venue_city, venue_name, venue_name)

    def extract_team_league_info(self, team):
        conference_id = team['conference']['id']
        conference_name = team['conference']['name']
        division_id = team['division']['id']
        division_name = team['division']['name']
        return self.create_nhl_team_info(conference_id, conference_name, division_id, division_name)

    def extract_standing_info(self, team_standing):
        info = {}
        info['team_id'] = int(team_standing['team']['id'])
        info['pts'] = int(team_standing['points'])
        info['win'] = int(team_standing['leagueRecord']['wins'])
        info['losses'] = int(team_standing['leagueRecord']['losses'])
        info['ot'] = int(team_standing['leagueRecord']['ot'])
        info['games_played'] = int(team_standing['gamesPlayed'])
        info['goals_against'] = int(team_standing['goalsAgainst'])
        info['goals_scored'] = int(team_standing['goalsScored'])
        return info

    def extract_ranks(self, team_standing):
        # ranks = {}
        league_rank = int(team_standing['leagueRank'])
        conference_rank = int(team_standing['conferenceRank'])
        division_rank = int(team_standing['divisionRank'])
        wildCard_rank = int(team_standing['wildCardRank'])
        return self.create_nhl_ranks(league_rank, conference_rank, division_rank, wildCard_rank)

    def create_nhl_team_info(self, conference_id, conference_name, division_id, division_name):
        info = {}
        info['conference'] = {'id': conference_id, 'name': conference_name}
        info['division'] = {'id': division_id, 'name': division_name}
        return info

    def create_nhl_ranks(self, league_rank, conference_rank, division_rank, wildCard_rank):
        rank = {}
        rank['league_rank'] = league_rank
        rank['conference_rank'] = conference_rank
        rank['division_rank'] = division_rank
        rank['wildCard_rank'] = wildCard_rank
        return rank

    def get_teams(self):
        nhl_teams = self._nhl_data.get_teams()
        db_teams = {}
        for tid in nhl_teams:
            t = nhl_teams[tid]['info']

            info = self.extract_team_info(t)
            venue = self.extract_team_venue(t)
            league_info = self.extract_team_league_info(t)
            team = self._pool_data.create_team(tid, info['abbreviation'], info['name'], info['fullname'],
                                               info['city'], info['active'], info['creation_year'],
                                               info['website'], venue, league_info)
            db_teams[tid] = team
        return db_teams

    def get_standings(self):
        nhl_standings = self._nhl_data.get_standings()
        db_standings = {}
        for division in nhl_standings:
            for team_standing in division['teamRecords']:
                info = self.extract_standing_info(team_standing)
                ranks = self.extract_ranks(team_standing)
                standing = self._pool_data.create_standings(info['team_id'], info['pts'], info['win'],
                                                            info['losses'], info['ot'], info['games_played'],
                                                            info['goals_against'], info['goals_scored'], ranks)
                db_standings[info['team_id']] = standing
        return db_standings

    def get_data(self):
        pass  # data = {}
