from pooldata.matchuptree import MatchupTree, STATE_NOT_STARTED
import unittest


class TestMatchupTreeMethods(unittest.TestCase):

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

    def create_tree(self):
        tree = MatchupTree()
        tree.create_node('t1', 2, next=None, state=STATE_NOT_STARTED)
        tree.create_node('t2', 1, next=tree.t1, state=STATE_NOT_STARTED)
        tree.create_node('t3', 1, next=tree.t1, state=STATE_NOT_STARTED)
        tree.update_node_links('t1', tree.t2, tree.t3)
        return tree

    def test_create_node(self):
        tree = self.create_tree()
        self.assertEqual(tree.t1.id, 't1')
        self.assertEqual(tree.t1.round, 2)
        self.assertEqual(tree.t1.state, STATE_NOT_STARTED)
        self.assertEqual(tree.t1.right, tree.t2)
        self.assertEqual(tree.t1.left, tree.t3)
        self.assertIsNone(tree.t1.next)
        self.assertIsNone(tree.t1.matchup)

    def test_set_get_items(self):
        tree = self.create_tree()
        self.assertEqual(tree['t1'].id, 't1')

    def test_set_error_items(self):
        tree = self.create_tree()
        with self.assertRaises(AttributeError):
            tree.t1 = 12
        with self.assertRaises(AttributeError):
            tree['12'] = 12

    def test_set_get_attr(self):
        tree = self.create_tree()
        self.assertEqual(tree.t1.id, 't1')

    def test_keys(self):
        tree = self.create_tree()
        self.assertEqual(len(tree.keys()), 3)

    def test_data(self):
        tree = self.create_tree()
        self.assertIsInstance(tree.data, dict)


if __name__ == '__main__':
    unittest.main()
