import os

from dotenv import load_dotenv
import jwt
from pwdlib import PasswordHash

load_dotenv()

password_hash = PasswordHash.recommended()


def hash_password(password):
    return password_hash.hash(password)


def verify_password(password, hash):
    return password_hash.verify(password, hash)
