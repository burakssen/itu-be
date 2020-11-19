import hashlib
import os

def hash_password(password):
    pass_salt = os.urandom(32)
    password_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),pass_salt,100000) 
    user = pass_salt + password_key
    return user

def hash_control(user_password, user):
    new_key = hashlib.pbkdf2_hmac('sha256', user_password.encode('utf-8'),user[:32],100000) 
    if new_key == user[32:]:
        return True
    else:
        return False