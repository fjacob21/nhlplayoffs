from powerdict import PowerDict


class TeamVenue(PowerDict):

    def __init__(self, city='', name='', timezone='', address=''):
        venue = {}
        venue['city'] = city
        venue['name'] = name
        venue['timezone'] = timezone
        venue['address'] = address
        self._data = venue
