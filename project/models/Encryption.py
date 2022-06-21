from cryptography.fernet import Fernet
from project.config.Database import mysql
import bcrypt
from bcrypt import hashpw
from datetime import datetime

class Encryption:   
    def encrypt(message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    def decrypt(token, email):
        f = Fernet(token)
        return f.decrypt(email.encode())

    def checkEmail(email):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email_user=%s", (email,))

        if cur.fetchone():
            return True
        else:
            return False
    
    def changePassword(email, password):
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        updated_at = datetime.now()
        update = mysql.connection.cursor()
        sql_update = "UPDATE users SET password=%s, updated_at=%s  WHERE email_user=%s"
        value = (hash_password, updated_at, email)
        update.execute(sql_update, value)
        mysql.connection.commit()
        return True
    