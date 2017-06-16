import unittest
import json
from powerdict import PowerDict, PowerDictEncoder, PowerDictDecoder


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

    def test_json(self):
        testdict = PowerDict()
        testdict.test = 12
        testdict['test2'] = 'test'
        tjson = json.dumps(testdict, cls=PowerDictEncoder)
        dec_testdict = json.loads(tjson, cls=PowerDictDecoder)
        self.assertIsInstance(dec_testdict, PowerDict)
        self.assertEqual(dec_testdict.test, testdict.test)
        self.assertEqual(dec_testdict['test2'], testdict['test2'])


if __name__ == '__main__':
    unittest.main()
