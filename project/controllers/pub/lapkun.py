from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
"""
    Import MOdels
from project.models.Hello import Hello
"""

# route index

@app.route("/laporankunjungan/")
def lapkun():
    title = ('LAPORAN KUNJUNGAN')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_lapkun as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY a.created_at DESC")
    data = cur.fetchall()
    return render_template("/public/lapkun/index.html", data=data, title=title)

@app.route("/laporankunjungan/thread/<int:id>")
def lapkun_thread(id):
    title = ('LAPORAN KUNJUNGAN')
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM tbl_lapkun as a LEFT JOIN users as b ON a.user_id = b.user_id WHERE a.lapkun_id=%s", (id,))
    data = cur.fetchone()
    return render_template("/public/lapkun/thread.html", data=data, title=title)

@app.route("/laporankunjungan/tambahlaporan", methods=["GET", "POST"])
def tambahlaporan():
    title = ("LAPORAN KUNJUNGAN")
    if request.method == 'GET':
        return render_template('public/lapkun/tambahlaporan.html', title=title)
    else:
        author = session['id']
        judul = request.form['judul-laporan']
        isi = request.form['isi-laporan']
        waktu = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_lapkun (user_id, lapkun_judul, lapkun_isi, created_at) VALUES (%s,%s,%s,%s)",
                    (author, judul, isi, waktu))
        mysql.connection.commit()
    return redirect(url_for('lapkun'))