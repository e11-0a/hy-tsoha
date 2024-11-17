from argon2 import PasswordHasher
from config import config

ph = PasswordHasher()

def tryHash(pw):
    if len(pw) > int(config["security"]["argon2_max"]):
        raise ValueError("Password too long for argon2")
    return ph.hash(pw)

def tryVerify(hash, pw):
    if len(pw) > int(config["security"]["argon2_max"]):
        raise ValueError("Password too long for argon2")
    return ph.verify(hash, pw)