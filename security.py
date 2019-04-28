from models.users import UserModel
from werkzeug.security import safe_str_cmp
import hashlib
import uuid


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return safe_str_cmp(password,hashlib.sha256(salt.encode() + user_password.encode()).hexdigest())


def authentication(username,password):
     user = UserModel.find_by_username(username)
     if user and check_password(user.password,password):
        # print('is here')
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
