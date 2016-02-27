import hashlib


USERS_DB = [
    'cabaco',
    'rex',
    'dinomonstro',
]

KEY_DB = [
    '57b76ecefbdc4d2f43939558ea05d24b',    # 1234
    'f8dbc001f904793e32e03c1a75e32d41',    # 5678
    '42bffe3e389f6400674471ab77a8b507',    # beico
]


def show():
    for lol in USERS_DB:
        return lol


def adduser(user, key):
    USERS_DB.append(user)
    passw = hashlib.md5(str(key) + "lolzinho")
    key = passw.hexdigest()
    KEY_DB.append(key)
    return 1


def trylogin(user, key):
    password = hashlib.md5(str(key) + "lolzinho")
    key = password.hexdigest()
    i = 0
    for nick in USERS_DB:
        if nick == user:
            if KEY_DB[i] == key:
                return 1
            else:
                return 0
        else:
            i = i+1
    return -1
