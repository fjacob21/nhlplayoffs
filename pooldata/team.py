from powerdict import PowerDict


class Team(PowerDict):

    def __init__(self, id=0, abbreviation='', name='', fullname='', city='', active=False, creation_year=0, website='', venue=None, league_info=None):
        team = {}
        team['id'] = id
        team['abbreviation'] = abbreviation
        team['name'] = name
        team['fullname'] = fullname
        team['city'] = city
        team['active'] = active
        team['creation_year'] = creation_year
        team['website'] = website
        team['venue'] = venue
        team['league_info'] = league_info
        self._data = team
