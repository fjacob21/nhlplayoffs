class PowerDict(object):

    def __init__(self):
        self._data = {}

    def keys(self):
        return self._data.keys()

    @property
    def data(self):
        return self._data

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __setattr__(self, name, value):
        if name != '_data':
            self._data[name] = value
        else:
            return object.__setattr__(self, name, value)

    def __getattr__(self, key):
        return self._data[key]

    def __repr__(self):
        return self._data.__repr__()

    def __str__(self):
        return self._data.__str__()
