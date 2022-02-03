from sqlalchemy import true
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
import bcrypt

@app.route("/dashboard/anggota")
def cp_anggota():
    title = ("TAMBAH ANGGOTA")
    if 'loggedin' in session and session['role'] == 2 and session['role'] == 1:
        par = mysql.connection.cursor()
        par.execute("SELECT users.nama_user, users.email_user, tbl_partai.nama_partai FROM users JOIN tbl_partai \
                     WHERE users.partai_id = tbl_partai.partai_id ORDER BY users.created_at DESC")
        data = par.fetchall()
        return render_template('panel/cp_anggota/index.html', data=data, title=title)
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            return redirect(url_for('login'))
    

@app.route("/dashboard/anggota/tambah", methods=["GET", "POST"])
def tambahanggota(): 
    if request.method == 'GET' and 'loggedin' in session and session['role'] == 2 and session['role'] == 1:
        return render_template('panel/cp_anggota/tambah.html')
    else:
        if 'loggedin' in session and session['role'] == 2 and session['role'] == 1: 
            nameAnggota = request.form['nameAnggota']
            emailAnggota = request.form['emailAnggota']
            passwordAnggota = request.form['passwordAnggota'].encode('utf-8')
            hash_password = bcrypt.hashpw(passwordAnggota, bcrypt.gensalt())
            role_id = 3
            partai = session['partai']
            created = datetime.now()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (nama_user, email_user, password, role_id, partai_id, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
                        (nameAnggota, emailAnggota, hash_password, role_id, partai, created))
            mysql.connection.commit()
            return redirect(url_for('cp_anggota'))
        else:
            if 'loggedin' in session :
                return redirect(url_for('pub_home'))
            else:
                return redirect(url_for('login'))

@app.route("/dashboard/anggota/delete/<id>")
def hapus_anggota(id):
    if 'loggedin' in session and session['role'] == 2 and session['role'] == 1:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE forum_id=%s", (id,))
        mysql.connection.commit()
        return redirect(url_for('cp_forum'))
    return redirect(url_for('login'))