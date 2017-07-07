import unittest
from pooldata import PoolData
from pooldata import GAME_STATE_FINISHED


class TestPoolDataMethods(unittest.TestCase):

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
        data = PoolData()
        team = data.add_team(1, 'TAM', 'Team', 'Test team',
                                'City', True, 1900, 'http://tam.com')
        team.add_venue('City', 'City venue', 'America/New_York', '123 street')
        team.league_info = leagueinfo
        self.assertIsNotNone(data.teams[1])
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
        data = PoolData()
        standing = data.add_standing(2000, 1, 100, 50, 25, 25, 100, 500, 1000, ranks, extrainfo)
        self.assertIsNotNone(data.years[2000].standings[1])
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

    def test_matchups(self):
        data = PoolData()
        m1 = data.add_matchup(2000, 'm1', 1, 1, 2, '2017-04-10T00:41:45Z')
        extra_data = {'test': 'test'}
        gs = m1.add_season_game('2017-04-10T00:41:45Z', 1, 0, extra_data)
        gp = m1.add_playoff_game('2017-04-10T00:41:45Z', GAME_STATE_FINISHED, 1, 0, extra_data)
        self.assertIsNotNone(data.years[2000].matchups['m1'])
        self.assertEqual(m1.id, 'm1')
        self.assertEqual(m1.home, 1)
        self.assertEqual(m1.away, 2)
        self.assertEqual(m1.round, 1)
        self.assertEqual(m1.start, '2017-04-10T00:41:45Z')
        self.assertIsNotNone(m1.season.games[1])
        self.assertIsNotNone(gs.home, 1)
        self.assertIsNotNone(gs.away, 2)
        self.assertIsNotNone(gs.date, '2017-04-10T00:41:45Z')
        self.assertIsNotNone(gs.state, GAME_STATE_FINISHED)
        self.assertIsNotNone(gs.home_goal, 1)
        self.assertIsNotNone(gs.away_goal, 2)
        self.assertIsNotNone(gs.extra_data['test'], 'test')
        self.assertIsNotNone(m1.playoff.games[1])
        self.assertIsNotNone(gp.home, 1)
        self.assertIsNotNone(gp.away, 2)
        self.assertIsNotNone(gp.date, '2017-04-10T00:41:45Z')
        self.assertIsNotNone(gp.state, GAME_STATE_FINISHED)
        self.assertIsNotNone(gp.home_goal, 1)
        self.assertIsNotNone(gp.away_goal, 2)
        self.assertIsNotNone(gp.extra_data['test'], 'test')


if __name__ == '__main__':
    unittest.main()
