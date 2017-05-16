import unittest
import players
import stores


class TestPlayersMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        stores.set_type(stores.DB_TYPE_TEST)
        cls._db = stores.get()
        cls._db.connect()

    @classmethod
    def tearDownClass(cls):
        cls._db.disconnect()

    def setUp(self):
        pass

    def tearDown(self):
        players.remove('test')

    def test_userhash(self):
        self.assertEqual(players.userhash('test'), '8fbc292370bee35baa86c5932308347699576d5d5a4b14456c77d95917f2ae10')

    def test_pswhash(self):
        self.assertEqual(players.pswhash('test', 'test'), 'cc5c095b5d4c96ba0f3e42e9a275bb2172d35e00a23b08e1d7b1bdc9a6358cad')

    def test_pswcheck(self):
        players.add('test', 'test')
        self.assertTrue(players.pswcheck('test', 'test'))
        players.remove('test')

    def test_add(self):
        self.assertTrue(players.add('test', 'test'))
        players.remove('test')
        self.assertTrue(players.add('test', 'test', 'test@test.com'))
        players.remove('test')
        self.assertTrue(players.add('test', 'test', 'test@test.com', True))
        players.remove('test')

    def test_remove(self):
        players.add('test', 'test')
        self.assertTrue(players.remove('test'))

    def test_change_email(self):
        players.add('test', 'test')
        self.assertTrue(players.change_email('test', 'test@test.com'))
        players.remove('test')

    def test_change_psw(self):
        players.add('test', 'test')
        self.assertTrue(players.change_psw('test', 'test', 'test2'))
        self.assertTrue(players.change_psw('test', 'test', 'test2', True))
        players.remove('test')

    def test_update_last_login(self):
        players.add('test', 'test')
        self.assertTrue(players.update_last_login('test'))
        players.remove('test')

    def test_get_all_admin(self):
        players.add('test', 'test')
        self.assertTrue(len(players.get_all_admin()) > 0)
        players.remove('test')

    def test_get_all(self):
        players.add('test', 'test')
        self.assertTrue(len(players.get_all()) > 0)
        players.remove('test')

    def test_get(self):
        players.add('test', 'test')
        self.assertTrue(players.get('test'))
        players.remove('test')

    def test_is_valid_player(self):
        players.add('test', 'test')
        self.assertTrue(players.is_valid_player(players.userhash('test')))
        players.remove('test')

    def test_login(self):
        players.add('test', 'test')
        self.assertEqual(players.login('test', 'test'), players.userhash('test'))
        players.remove('test')

    def test_root_access(self):
        self.assertFalse(players.root_access('test'))


if __name__ == '__main__':
    unittest.main()
