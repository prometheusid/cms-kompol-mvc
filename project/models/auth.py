from flask_mysqldb import MySQL
from project import app
from flask_login import UserMixin

mysql = MySQL(app)

class User(UserMixin):
    curl = mysql.connection.cursor()
    curl.execute("SELECT * FROM mysql.users")
    user = curl.fetchone()
    curl.close()