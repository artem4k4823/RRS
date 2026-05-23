import bcrypt
from .token import decode_jwt

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(entered_password, hashed_password):
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8'))

        