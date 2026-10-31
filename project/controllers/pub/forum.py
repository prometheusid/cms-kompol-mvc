
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
"""
    Import MOdels
from project.models.Hello import Hello
"""
#route index
@app.route("/forum")
def forum():
    title = ("FORUM DISKUSI")
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * from tbl_forum as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY created_at DESC")
    data = cur.fetchall()
    return render_template('public/forum/index.html', data=data, title=title)

@app.route("/forum/thread/<int:id>")
def thread(id):
    title = ("FORUM DISKUSI")
    # if request.method == 'GET':
    # Get one data forum
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from tbl_forum as a \
                    LEFT JOIN tbl_detail_forum as b ON a.forum_id = b.forum_id \
                    LEFT JOIN users as c ON a.user_id = c.user_id WHERE a.forum_id=%s", (id,))
    data = cur.fetchone()

    # Get Count commentar
    count = mysql.connection.cursor()
    count.execute(
        "SELECT count('forum_id') FROM tbl_detail_forum  WHERE forum_id=%s", (id,))
    counting = count.fetchone()

    # Get data commentar
    com = mysql.connection.cursor()
    com.execute(
        "SELECT * FROM tbl_detail_forum as a JOIN users as b ON a.user_id = b.user_id WHERE a.forum_id=%s", (id,))
    comment = com.fetchall()
    return render_template('public/forum/thread.html', data=data, comment=comment, counting=counting,  title=title)

@app.route("/pub_forum/thread", methods=["POST"])
def komentar():
    idKomen = request.form['idKomen']
    idForum = request.form['idForum']
    komen = request.form['komen']
    komenUser = session['id']
    waktu = datetime.now()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tbl_detail_forum (id_detail_forum, forum_id, komentar, user_id, created_at) VALUES (%s,%s,%s,%s,%s)",
                (idKomen, idForum, komen, komenUser, waktu))
    mysql.connection.commit()
    return redirect(request.referrer)


@app.route("/pub_forum/tambah", methods=["GET", "POST"])
def tambahforum():
    title = ("FORUM DISKUSI")
    if request.method == 'GET':
        return render_template('public/forum/tambahforum.html', title=title)
    else:
        idForum = request.form['idForum']
        judulForum = request.form['judulForum']
        isi = request.form['content']
        ts = session['id']
        waktu = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_forum (forum_id, forum_judul, forum_isi, user_id, created_at) VALUES (%s,%s,%s,%s,%s)",
                    (idForum, judulForum, isi, ts, waktu))
        mysql.connection.commit()
        return redirect(url_for('forum'))
    return render_template('public/forum/tambahforum.html', title=title)


@app.route("/pub_forum/update/<int:id>", methods=["GET", "POST"])
def updateforum(id):
    title = ("FORUM DISKUSI")
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_forum WHERE forum_id=%s", (id,))
        data = cur.fetchone()
        return render_template('public/forum/update.html', data=data, title=title)
    else:
        return redirect(url_for('thread', id=id))

@app.route("/pub_forum/simpanupdate/<int:id>", methods=["GET", "POST"])
def simpanupdate(id):
    if request.method == "POST":
        fid = request.form['idForum']
        judulForum = request.form['judulForum']
        isi = request.form['content']
        ts = session['id']
        waktu = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tbl_forum SET forum_judul = %s, forum_isi = %s, user_id = %s, created_at = %s WHERE forum_id = %s",
                    (judulForum, isi, ts, waktu, fid))
        mysql.connection.commit()
        return redirect(url_for('forum'))
    else:
        title = ("FORUM DISKUSI")
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_forum WHERE forum_id=%s", (id,))
        data = cur.fetchone()
        return render_template("public/forum/thread.html", data=data, title=title)