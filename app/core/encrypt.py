import bcrypt

def encrypt_data(password): 
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)

def check_password(hash, input_password): 
    userBytes = input_password.encode('utf-8')
    return bcrypt.checkpw(userBytes, hash)
