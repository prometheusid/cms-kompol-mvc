"""
    Example Controllers
"""

from project import app
from flask import render_template, redirect, url_for, request, session
from datetime import datetime
from project.config.Database import mysql
"""
    Import MOdels
from project.models.Hello import Hello
"""
#index info
@app.route('/info', methods = ['GET'])
def info():
    title = ("INFO PUBLIK")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM info as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY a.created_at DESC")
    data = cur.fetchall()
    return render_template('public/info/index.html', data = data, title = title)

# Tambah Info
@app.route("/pub_info/tambahinfo", methods=["GET", "POST"])
def tambahinfo():
    title = ("INFO PUBLIK")
    if request.method == 'GET':
        return render_template('public/info/tambahinfo.html', title=title)
    else:
        author = session['id']
        judul = request.form['judul-info']
        isi = request.form['isi-info']
        waktu = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO info (user_id, judul_info, isi_info, created_at) VALUES (%s,%s,%s,%s)",
                    (author, judul, isi, waktu))
        mysql.connection.commit()
    return render_template('public/info/tambahinfo.html', title=title)

# Detail Info
@app.route('/info/detail/<int:id>')
def detailinfo(id):
    title = ("INFO PUBLIK")
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * from info as a LEFT JOIN users as b ON a.user_id = b.user_id WHERE a.info_id=%s", (id,))
    data = cur.fetchone()
    return render_template('public/info/detail.html', data=data, title=title)