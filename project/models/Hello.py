import mysql.connector, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL, MySQLdb
from project import app
"""
    Import local package

from project.config.Database import connection as con, cursor as cur
from project.config.DatetimeEncoder import DatetimeEncoder
from project.config.Hash import Hash
"""
"""
    Your Code
"""

db = SQLAlchemy(app)
mysql = MySQL(app)

class Hello:

    def get_info() :
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from info as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY created_at DESC")
        data = cur.fetchall()
    
    def __init__(self):
        pass
