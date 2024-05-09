import random
import bcrypt
def generate_password(length):
    password = ''
    for i in range(length):
        password += chr(random.randint(33, 126))
    return password

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    #load hash from string hashed
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))