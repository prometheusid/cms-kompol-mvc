from wsgiref.validate import PartialIteratorWrapper
from sqlalchemy import true
from project import app
from flask import render_template, redirect, url_for, request, session, flash
from project.config.Database import mysql
from flask_mysqldb import MySQLdb
from datetime import datetime
import bcrypt
import re

from project.models.Profile import Profile
from project.models.Anggota import Anggota

@app.route("/dashboard/anggota/partai/<partai>")           
def cp_anggota_partai(partai):
    title = ("TAMBAH ANGGOTA")
    if 'loggedin' in session and session['role'] == 2:
        par = mysql.connection.cursor()
        par.execute("SELECT * FROM tbl_partai a INNER JOIN users b ON a.partai_id=b.partai_id \
                     WHERE b.partai_id=%s", (partai,))
        data = par.fetchall()

        profile = Profile.editProfiles(id)

        edu = mysql.connection.cursor()
        edu.execute("SELECT * FROM tbl_pendidikan")
        edu = edu.fetchall()
        return render_template('panel/cp_partai/index.html', edu=edu, profile=profile, data=data, title=title)
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            return redirect(url_for('login'))

@app.route("/dashboard/anggota/partai")           
def cp_anggota_partai_edit():
    title = ("DETAIL ANGGOTA")
    if 'loggedin' in session and session['role'] == 2:
        name = request.form['name']
        update = datetime.now()
        education = request.form['education']
        pengalaman = request.form['pengalaman']
        twitter = request.form['twitter']
        idu = request.form['idu']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nama_user = %s, updated_at = %s, id_pendidikan = %s, pengalaman = %s, akun_twitter = %s WHERE user_id = %s",
                    (name, update, education, pengalaman, twitter, idu))
        mysql.connection.commit()
        return render_template('panel/cp_partai/index.html', title=title)
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            return redirect(url_for('login'))

@app.route("/dashboard/anggota/partai", methods=["GET", "POST"])
def tambahanggotapartai():
    if 'loggedin' in session and session['role'] == 2 and 'emailAnggota' in request.form and 'passwordAnggota' in request.form and 'nameAnggota' in request.form: 
        nameAnggota = request.form['nameAnggota']
        emailAnggota = request.form['emailAnggota']
        passwordAnggota = request.form['passwordAnggota'].encode('utf-8')
        hash_password = bcrypt.hashpw(passwordAnggota, bcrypt.gensalt())
        role_id = 3
        partai = session['partai']
        created = datetime.now()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email_user = %s', (emailAnggota,))
        account = cursor.fetchone()
        if account:
            flash(u'Account already exists!', 'danger')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailAnggota):
            flash(u'Invalid email address!', 'danger')
        elif not re.match(r'[A-Za-z0-9]+', nameAnggota):
            flash(u'Name must contain only characters!', 'danger')
        elif not nameAnggota or not passwordAnggota or not emailAnggota:
            flash(u'Please fill out the form!', 'danger')
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (nama_user, email_user, password, role_id, partai_id, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
                        (nameAnggota, emailAnggota, hash_password, role_id, partai, created))
            mysql.connection.commit()
            flash('Berhasil ditambahkan!', 'success')
    return redirect(url_for('cp_anggota_partai', partai=partai))

@app.route("/dashboard/anggota/partai/hapus/<id>")
def hapus_anggota_partai(id):
    data = Anggota.deleteAnggotaPartai(id)
    flash('Data telah dihapus!', 'danger')
    return redirect(url_for('cp_anggota_partai', partai=PartialIteratorWrapper))