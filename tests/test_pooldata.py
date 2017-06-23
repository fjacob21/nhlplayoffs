import unittest
from pooldata import PoolData


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


if __name__ == '__main__':
    unittest.main()
