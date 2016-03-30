# Players management module
#
import hashlib

players = {}
salt = 'superhero'

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

#add players
def add(name, psw, email='', admin=False):
    hname = userhash(name)
    if players.has_key(hname):
        return False
    hpsw = pswhash(name, psw)
    players[hname] = {'name':name, 'psw':hpsw, 'email':email, 'admin':admin}
    #Store in DB
    return True

#remove players
def remove(player):
    hname = userhash(player)
    if not players.has_key(hname):
        return False
    del players[hname]
    #Store in DB
    return True

def change_email(player, email):
    hname = userhash(player)
    if not players.has_key(hname):
        return False
    players[hname]['email'] = email
    #Store in DB
    return True

def change_psw(player, old, new):
    hname = userhash(player)
    if not players.has_key(hname):
        return False

    if not pswcheck(player, old):
        return False
    hpsw = pswhash(player, new)
    players[hname]['psw'] = hpsw
    #Store in DB
    return True

def get_all():
    l = list(players.values())
    result = []
    for player in l:
        p = player.copy()
        del p['psw']
        result.append(p)
    return result

def get(player):
    hname = userhash(player)
    if not players.has_key(hname):
        return None
    p = players[hname].copy()
    del p['psw']
    return p

def login(player, psw):
    hname = userhash(player)
    if not players.has_key(hname):
        return None
    if not pswcheck(player, psw):
        return None
    return hname
