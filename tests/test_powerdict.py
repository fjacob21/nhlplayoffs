import unittest
from powerdict import PowerDict


class TestPowerDictMethods(unittest.TestCase):

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

    def test_set_get_items(self):
        testdict = PowerDict()
        testdict['test'] = 12
        self.assertEqual(testdict['test'], 12)
        testdict['test2'] = 'test'
        self.assertEqual(testdict['test2'], 'test')

    def test_set_get_attr(self):
        testdict = PowerDict()
        testdict.test = 12
        self.assertEqual(testdict.test, 12)
        testdict.test2 = 'test'
        self.assertEqual(testdict.test2, 'test')

    def test_keys(self):
        testdict = PowerDict()
        testdict['test'] = 12
        self.assertEqual(testdict.keys(), ['test'])

    def test_data(self):
        testdict = PowerDict()
        testdict['test'] = 12
        self.assertEqual(testdict.data, {'test': 12})


if __name__ == '__main__':
    unittest.main()
