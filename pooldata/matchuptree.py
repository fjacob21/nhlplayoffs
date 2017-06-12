from powerdict import PowerDict


class MatchupTree(object):
    STATE_UNITIALIZED = 1
    STATE_NOT_STARTED = 2
    STATE_STARTED = 3
    STATE_FINISHED = 4

    def __init__(self):
        self._nodes = {}
        self._on_matchup_finished = None
        self._on_round_finished = None

    def create_node(self, id, round, right=None, left=None, next=None, matchup=None, state=STATE_UNITIALIZED):
        self._nodes[id] = MatchupTreeNode(id, round, right, left, next, matchup, state)

    def update_node_state(self, id, state):
        self._nodes[id]['state'] = state

    def update_node_links(self, id, right=None, left=None, next=None):
        if right:
            self._nodes[id]['right'] = right
        if left:
            self._nodes[id]['left'] = left
        if next:
            self._nodes[id]['next'] = next

    def get_started_nodes(self):
        started = []
        for node in self._nodes.values():
            if node['state'] == MatchupTree.STATE_STARTED:
                started.append(node)
        return started

    def keys(self):
        return self._nodes.keys()

    def __getitem__(self, key):
        return self._nodes[key]

    def __getattr__(self, key):
        return self._nodes[key]


class MatchupTreeNode(PowerDict):

    def __init__(self, id, round, right=None, left=None, next=None, matchup=None, state=MatchupTree.STATE_UNITIALIZED):
        node = {}
        node['id'] = id
        node['round'] = round
        node['state'] = state
        node['right'] = right
        node['left'] = left
        node['next'] = next
        node['matchup'] = matchup
        self._data = node
