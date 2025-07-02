import bcrypt

def encrypt_data(password): 
    encoded_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_password, salt).decode('utf-8')

def check_password(hash, input_password): 
    user_bytes = input_password.encode('utf-8')
    hash_bytes = hash.encode('utf-8')
    return bcrypt.checkpw(user_bytes, hash_bytes)