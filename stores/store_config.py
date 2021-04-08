import json

class StoreConfig(object):

    def __init__(self, file="/etc/nhlplayoffs/store.json"):
        self._file = file
        self._store = "memory"
        self._user = ""
        self._password = ""
        self._database = ""
        self._server = ""
        self._port = 5432
        self.load()
    
    @property
    def store(self):
        return self._store
    
    @property
    def user(self):
        return self._user
    
    @property
    def password(self):
        return self._password
    
    @property
    def database(self):
        return self._database
    
    @property
    def server(self):
        return self._server
    
    @property
    def port(self):
        return self._port
    
    def load(self):
        try:
            with open(self._file, "rt") as f:
                data = json.load(f)
                self._store = data["store"]
                self._user = data["user"]
                self._password = data["password"]
                self._database = data["database"]
                self._server = data["server"]
                self._port = int(data["port"])
                
        except Exception as e:
            raise e
