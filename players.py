# Players management module
#
import hashlib
from postgres_store import postgres_store

#players = {}
salt = 'superhero'
_db = postgres_store('fred', 'fred', '763160', 'localhost', 5432)

def userhash(name):
    hash = hashlib.sha256()
    hash.update(salt + name)
    return hash.hexdigest()

def pswhash(name, psw):
    hash = hashlib.sha256()
    hash.update(salt + name + psw)
    return hash.hexdigest()

def pswcheck(player, psw):
    hname = userhash(player)
    if not players.has_key(hname):
        return False
    hpsw = pswhash(player, psw)
    return hpsw == players[hname]['psw']

def restore_db():
    players = _db.restore('players', 1)
    if players == '':
        players = {}
    return players

def store_db(players):
    return _db.store('players', 1, players)

#add players
def add(name, psw, email='', admin=False):
    players = restore_db()
    hname = userhash(name)
    if players.has_key(hname):
        return False
    hpsw = pswhash(name, psw)
    players[hname] = {'name':name, 'psw':hpsw, 'email':email, 'admin':admin}
    #Store in DB
    return store_db(players)

#remove players
def remove(player):
    players = restore_db()
    hname = userhash(player)
    if not players.has_key(hname):
        return False
    del players[hname]
    #Store in DB
    return store_db(players)

def change_email(player, email):
    players = restore_db()
    hname = userhash(player)
    if not players.has_key(hname):
        return False
    players[hname]['email'] = email
    #Store in DB
    return store_db(players)

def change_psw(player, old, new):
    players = restore_db()
    hname = userhash(player)
    if not players.has_key(hname):
        return False

    if not pswcheck(player, old):
        return False
    hpsw = pswhash(player, new)
    players[hname]['psw'] = hpsw
    #Store in DB
    return store_db(players)

def get_all():
    players = restore_db()
    l = list(players.values())
    result = []
    for player in l:
        p = player.copy()
        del p['psw']
        result.append(p)
    return result

def get(player):
    players = restore_db()
    hname = userhash(player)
    if not players.has_key(hname):
        return None
    p = players[hname].copy()
    del p['psw']
    return p

def is_valid_player(hplayer):
    players = restore_db()
    return players.has_key(hplayer):

def login(player, psw):
    players = restore_db()
    hname = userhash(player)
    if not players.has_key(hname):
        return None
    if not pswcheck(player, psw):
        return None
    return hname
