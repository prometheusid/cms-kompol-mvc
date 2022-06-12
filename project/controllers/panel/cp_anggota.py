from functools import partial
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

@app.route("/dashboard/anggota/<id>")
def cp_anggota(id):
    title = ("ANGGOTA")
    if 'loggedin' in session and session['role'] == 1:
        par = mysql.connection.cursor()
        par.execute("SELECT users.user_id, users.nama_user, users.email_user, users.pengalaman, users.akun_twitter, tbl_partai.nama_partai FROM users JOIN tbl_partai \
                     WHERE users.partai_id=tbl_partai.partai_id ORDER BY users.created_at DESC")
        data = par.fetchall()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users JOIN tbl_partai \
                     WHERE users.partai_id = tbl_partai.partai_id ORDER BY users.created_at DESC")
        profile = cur.fetchone()

        edu = mysql.connection.cursor()
        edu.execute("SELECT * FROM tbl_pendidikan")
        edu = edu.fetchall()
        
        return render_template('panel/cp_anggota/index.html', data=data, edu=edu, profile=profile, title=title)
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            flash('Silahkan login terlebih dahulu!', 'danger')
            return redirect(url_for('login'))

@app.route("/dashboard/anggota", methods=["GET", "POST"])
def tambahanggota(): 
    if 'loggedin' in session and session['role'] == 1 and 'emailAnggota' in request.form and 'passwordAnggota' in request.form and 'nameAnggota' in request.form: 
        nameAnggota = request.form['nameAnggota']
        emailAnggota = request.form['emailAnggota']
        passwordAnggota = request.form['passwordAnggota'].encode('utf-8')
        hash_password = bcrypt.hashpw(passwordAnggota, bcrypt.gensalt())
        role_id = request.form['roleAnggota']
        partai = request.form['partaiAnggota']
        education = request.form['education']
        pengalaman = request.form['pengalaman']
        twitter = request.form['twitter']
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
            cur.execute("INSERT INTO users (nama_user, email_user, password, role_id, partai_id, created_at, id_pendidikan, pengalaman, akun_twitter) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (nameAnggota, emailAnggota, hash_password, role_id, partai, created, education, pengalaman, twitter))
            mysql.connection.commit()
            flash('Berhasil ditambahkan!', 'success')
    return redirect(url_for('cp_anggota', id=id))

@app.route("/dashboard/anggota/<id>", methods=["GET", "POST"])           
def editAnggota(id):
    if 'loggedin' in session and session['role'] == 1:
        idu = request.form['idu']
        name = request.form['name']
        education = request.form['education']
        pengalaman = request.form['pengalaman']
        twitter = request.form['twitter']
        update = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nama_user = %s, id_pendidikan = %s, pengalaman = %s, akun_twitter = %s, updated_at = %s WHERE user_id = %s",
                    (name, education, pengalaman, twitter, update, idu))
        mysql.connection.commit()
        flash('Data berhasil diubah!', 'success')
        #return render_template('panel/cp_partai/index.html', title=title)
        return redirect(url_for('cp_anggota', id=id))
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            flash('Silahkan login terlebih dahulu!', 'danger')
            return redirect(url_for('login'))

@app.route("/dashboard/anggota/hapus/<id>")
def hapus_anggota(id):
    if 'loggedin' in session and session['role'] == 1 and session['id']:
        data = Anggota.deleteAnggota(id)
        flash('Data telah dihapus!', 'danger')
        return redirect(url_for('cp_anggota', id=id))