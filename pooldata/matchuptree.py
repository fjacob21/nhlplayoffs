from powerdict import PowerDict

STATE_UNITIALIZED = 1
STATE_NOT_STARTED = 2
STATE_STARTED = 3
STATE_FINISHED = 4


class MatchupTree(object):

    def __init__(self):
        self._nodes = {}
        self._on_matchup_finished = None
        self._on_round_finished = None

    def create_node(self, id, round, right=None, left=None, next=None, matchup=None, state=STATE_UNITIALIZED):
        self._nodes[id] = MatchupTreeNode(id, round, right, left, next, matchup, state)

    def update_node_links(self, id, right=None, left=None, next=None):
        if right:
            self._nodes[id]['right'] = right
        if left:
            self._nodes[id]['left'] = left
        if next:
            self._nodes[id]['next'] = next

    def keys(self):
        return self._nodes.keys()

    @property
    def data(self):
        return self._nodes

    def __getitem__(self, key):
        return self._nodes[key]

    def __setitem__(self, key, value):
        raise AttributeError("Invalid node id: '" + key + "'")

    def __contains__(self, key):
        return key in self._nodes

    def __getattr__(self, key):
        return self._nodes[key]

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            raise AttributeError("Invalid node id: '" + name + "'")
        else:
            return object.__setattr__(self, name, value)


class MatchupTreeNode(PowerDict):

    def __init__(self, id, round, right=None, left=None, next=None, matchup=None, state=STATE_UNITIALIZED):
        node = {}
        node['id'] = id
        node['round'] = round
        node['state'] = state
        node['right'] = right
        node['left'] = left
        node['next'] = next
        node['matchup'] = matchup
        self._data = node
