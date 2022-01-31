# import mysql.connector

# connection = mysql.connector(
#     host = "localhost",
#     user = "root",
#     password = "",
#     db = "db_kompol"
# )

# cursor = connection.cursor()
from flask_mysqldb import MySQL, MySQLdb
from project import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+MySQLdb://root:@localhost/db_kompol'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_kompol'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

mysql = MySQL(app)