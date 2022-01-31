from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
"""
    Import MOdels
from project.models.Hello import Hello
"""
@app.route('/dashboard/cp_info')
def cp_info():
    title = ('INFO PUBLIK')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM info as a join users as b on a.user_id = b.user_id")
    data = cur.fetchall()
    return render_template('panel/cp_info/index.html', data=data, title=title)


@app.route("/dashboard/cp_info/delete/<int:id>")
def hapus_info(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM info WHERE info_id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('cp_info'))