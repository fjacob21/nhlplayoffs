from datetime import datetime
from dateutil import tz
import unittest
import pooldata.pooldatafactory as pooldatafactory
from pooldata import GAME_STATE_FINISHED


class TestPoolDataFactoryMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_team(self):
        leagueinfo = {'league': 'testleague'}
        teamvenue = pooldatafactory.create_team_venue('City', 'City venue', 'America/New_York', '123 street')
        team = pooldatafactory.create_team(1, 'TAM', 'Team', 'Test team',
                                           'City', True, 1900, 'http://tam.com',
                                           teamvenue, leagueinfo)
        self.assertEqual(team.id, 1)
        self.assertEqual(team.abbreviation, 'TAM')
        self.assertEqual(team.name, 'Team')
        self.assertEqual(team.fullname, 'Test team')
        self.assertEqual(team.city, 'City')
        self.assertEqual(team.active, True)
        self.assertEqual(team.creation_year, 1900)
        self.assertEqual(team.website, 'http://tam.com')
        self.assertEqual(team.venue.city, 'City')
        self.assertEqual(team.venue.name, 'City venue')
        self.assertEqual(team.venue.timezone, 'America/New_York')
        self.assertEqual(team.venue.address, '123 street')
        self.assertEqual(team.league_info['league'], 'testleague')

    def test_standing(self):
        ranks = {'league': 1}
        extrainfo = {'info': 'info'}
        standing = pooldatafactory.create_standing(1, 100, 50, 25, 25, 100, 500, 1000, ranks, extrainfo)
        self.assertEqual(standing.team_id, 1)
        self.assertEqual(standing.pts, 100)
        self.assertEqual(standing.win, 50)
        self.assertEqual(standing.losses, 25)
        self.assertEqual(standing.ot, 25)
        self.assertEqual(standing.games_played, 100)
        self.assertEqual(standing.goals_against, 500)
        self.assertEqual(standing.goals_scored, 1000)
        self.assertEqual(standing.ranks['league'], 1)
        self.assertEqual(standing.extra_info['info'], 'info')

    def test_matchup(self):
        extradata = {'extra': 'data'}
        schedule = [pooldatafactory.create_matchup_game(1, 2, '2017-04-10T00:41:45Z', GAME_STATE_FINISHED, 1, 0, extradata)]
        seasonresults = pooldatafactory.create_matchup_season_results(1, 0, schedule)
        results = pooldatafactory.create_matchup_results(1, 0)
        matchup = pooldatafactory.create_matchup('m', 1, 1, 2, '', schedule, seasonresults, results)
        self.assertEqual(matchup.id, 'm')
        self.assertEqual(matchup.round, 1)
        self.assertEqual(matchup.home, 1)
        self.assertEqual(matchup.away, 2)
        self.assertEqual(matchup.start, '')
        self.assertEqual(matchup.schedule[0].home, 1)
        self.assertEqual(matchup.schedule[0].away, 2)
        self.assertEqual(matchup.schedule[0].date, '2017-04-10T00:41:45Z')
        self.assertEqual(matchup.schedule[0].state, GAME_STATE_FINISHED)
        self.assertEqual(matchup.schedule[0].home_goal, 1)
        self.assertEqual(matchup.schedule[0].away_goal, 0)
        self.assertEqual(matchup.schedule[0].extra_data['extra'], 'data')
        self.assertEqual(matchup.season_results.home_win, 1)
        self.assertEqual(matchup.season_results.away_win, 0)
        self.assertEqual(matchup.season_results.games[0].home, 1)
        self.assertEqual(matchup.season_results.games[0].away, 2)
        self.assertEqual(matchup.season_results.games[0].date, '2017-04-10T00:41:45Z')
        self.assertEqual(matchup.season_results.games[0].state, GAME_STATE_FINISHED)
        self.assertEqual(matchup.season_results.games[0].home_goal, 1)
        self.assertEqual(matchup.season_results.games[0].away_goal, 0)
        self.assertEqual(matchup.season_results.games[0].extra_data['extra'], 'data')
        self.assertEqual(matchup.results.home_win, 1)
        self.assertEqual(matchup.results.away_win, 0)

    def test_date(self):
        date = "2017-04-10T00:41:45Z"
        self.assertTrue(isinstance(pooldatafactory.now(), datetime))
        self.assertEqual(pooldatafactory.date_to_string(pooldatafactory.string_to_date(date)), date)
        self.assertEqual(pooldatafactory.date_to_string(pooldatafactory.date(2017, 4, 10, 0, 41, 45, tzinfo=tz.gettz('UTC'))), date)


if __name__ == '__main__':
    unittest.main()
