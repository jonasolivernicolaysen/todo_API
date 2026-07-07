import bcrypt

password = b"password"

salt = bcrypt.gensalt()

hashed = bcrypt.hashpw(password, salt=salt)
print(salt)
print(hashed)

def hashPassword(password: str):
    password_as_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_as_bytes, salt=salt)
    return hashed_password

def checkPassword(password: str, stored_password: bytes):
    entered_password = password.encode("utf-8")
    if bcrypt.checkpw(entered_password, stored_password):
        return True
    return False