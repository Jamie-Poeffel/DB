from bcrypt import hashpw, gensalt, checkpw

def check_password(stored_hash, password):
    return checkpw(password.encode('utf-8'), stored_hash)

def hash_password(password):
    # Erzeuge ein Salt
    salt = gensalt()
    # Hash das Passwort mit dem Salt
    hashed = hashpw(password.encode('utf-8'), salt)
    return hashed