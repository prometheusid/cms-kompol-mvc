from sqlalchemy import true
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
import bcrypt

@app.route("/dashboard/anggota")
def cp_anggota():
    title = ("TAMBAH ANGGOTA")
    if 'loggedin' in session and session['role'] == 1:
        par = mysql.connection.cursor()
        par.execute("SELECT a.user_id, a.nama_user, a.email_user, b.nama_partai FROM users as A JOIN tbl_partai as b ON a.partai_id = b.partai_id WHERE a.role_id = 3 ORDER BY a.created_at DESC")
        data = par.fetchall()
        return render_template('panel/cp_anggota/index.html', data=data, title=title)
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            return redirect(url_for('login'))
    

@app.route("/dashboard/anggota", methods=["GET", "POST"])
def tambahanggota(): 
    if 'loggedin' in session and session['role'] == 1: 
        nameAnggota = request.form['nameAnggota']
        emailAnggota = request.form['emailAnggota']
        passwordAnggota = request.form['passwordAnggota'].encode('utf-8')
        hash_password = bcrypt.hashpw(passwordAnggota, bcrypt.gensalt())
        role_id = request.form['roleAnggota']
        partai = request.form['partaiAnggota']
        created = datetime.now()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (nama_user, email_user, password, role_id, partai_id, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
                        (nameAnggota, emailAnggota, hash_password, role_id, partai, created))
        mysql.connection.commit()
    return redirect(url_for('cp_anggota'))

@app.route("/dashboard/anggota/delete/<int:id>")
def hapus_anggota(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE user_id=%s" % (id))
    mysql.connection.commit()
    return redirect(url_for('cp_anggota'))