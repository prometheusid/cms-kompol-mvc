"""
    Example Controllers
"""

from project import app
from flask import render_template, redirect, url_for
from project.config.Database import mysql
# from flask_mysqldb import MySQL, MySQLdb
# mysql = MySQL(app)
"""
    Import MOdels
from project.models.Hello import Hello
"""

# from project.models.Hello import Hello
#route index
@app.route('/test', methods = ['GET'])
def index():
    title = ("INFO PUBLIK")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from info as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY created_at DESC")
    data = cur.fetchall()
    return render_template('index.html.j2', data = data, title = title)
