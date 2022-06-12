from functools import partial
from http.client import PARTIAL_CONTENT
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
    title = ("ANGGOTA PARTAI")
    if 'loggedin' in session and session['role'] == 2:
        par = mysql.connection.cursor()
        par.execute("SELECT * FROM tbl_partai a INNER JOIN users b ON a.partai_id=b.partai_id \
                     JOIN role_users c ON b.role_id=c.role_id \
                     WHERE b.partai_id=%s ORDER BY b.created_at DESC", (partai,))
        data = par.fetchall()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users JOIN role_users ON role_users.role_id=users.role_id \
                    LEFT JOIN tbl_partai ON tbl_partai.partai_id=users.partai_id \
                    WHERE users.partai_id=%s", (partai,))
        profile = cur.fetchone()

        edu = mysql.connection.cursor()
        edu.execute("SELECT * FROM tbl_pendidikan a JOIN users b ON a.id_pendidikan=b.id_pendidikan \
                     WHERE b.partai_id=%s", (partai,))
        edu = edu.fetchall()

        edus = mysql.connection.cursor()
        edus.execute("SELECT * FROM tbl_pendidikan")
        edus = edus.fetchall()
        return render_template('panel/cp_partai/index.html', edus=edus, edu=edu, profile=profile, data=data, title=title)
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            return redirect(url_for('login'))

@app.route("/dashboard/anggota/partai/<partai>", methods=["GET", "POST"])           
def cp_anggota_partai_edit(partai):
    if 'loggedin' in session and session['role'] == 2:
        idu = request.form['idu']
        nameAnggota = request.form['nameAnggota']
        education = request.form['education']
        pengalaman = request.form['pengalaman']
        twitter = request.form['twitter']
        update = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nama_user = %s, id_pendidikan = %s, pengalaman = %s, akun_twitter = %s, updated_at = %s WHERE user_id = %s",
                    (nameAnggota, education, pengalaman, twitter, update, idu))
        mysql.connection.commit()
        flash('Data berhasil diubah!', 'success')
        return redirect(url_for('cp_anggota_partai', partai=partai))
    else: 
        if 'loggedin' in session :
            return redirect(url_for('pub_home'))
        else:
            flash('Silahkan login terlebih dahulu!', 'danger')
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
        pengalaman = request.form['pengalaman']
        education = request.form['education']
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
    return redirect(url_for('cp_anggota_partai', partai=partai))

@app.route("/dashboard/anggota/partai/hapus/<partai>/<id>")
def hapus_anggota_partai(partai, id):
    if 'loggedin' in session and session['role'] == 2 and session['partai']:
        data = Anggota.deleteAnggotaPartai(id)
        flash('Data telah dihapus!', 'danger')
        return redirect(url_for('cp_anggota_partai', partai=partai))