# Players management module
#
import hashlib
import postgres_store

salt = 'superhero'
_db = postgres_store.get_default()

def userhash(name):
    hash = hashlib.sha256()
    hash.update(salt + name)
    return hash.hexdigest()

def pswhash(name, psw):
    hash = hashlib.sha256()
    hash.update(salt + name + psw)
    return hash.hexdigest()

def pswcheck(player, psw):
    players = _db.restore('players', 1)
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

def get_all_admin():
    players = restore_db()
    l = list(players.items())
    result = []
    for player in l:
        p = player[1].copy()
        del p['psw']
        p['id'] = player[0]
        result.append(p)
    return result

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
    return hplayer in players

def login(player, psw):
    players = restore_db()
    hname = userhash(player)
    if not players.has_key(hname):
        return None
    if not pswcheck(player, psw):
        return None
    return hname
