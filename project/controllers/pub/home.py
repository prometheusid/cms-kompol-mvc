
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
"""
    Import MOdels
from project.models.Hello import Hello
"""
#route index
@app.route('/', methods = ['GET'])
def pub_home():
    title = ("KOMUNIKASI POLITIK")
    """ cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM info ORDER BY info_id DESC LIMIT 1")
    info = cur.fetchone()
    cur.execute("SELECT * FROM tbl_forum ORDER BY forum_id DESC LIMIT 1")
    data = cur.fetchone() """
    return render_template('public/homepage/index.html', title=title)
