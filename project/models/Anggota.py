from project.config.Database import mysql
from datetime import datetime
from flask import request, flash
import bcrypt
from flask_mysqldb import MySQLdb
import re

class Anggota:

    def semuaAnggota():
        par = mysql.connection.cursor()
        par.execute("SELECT users.user_id, users.nama_user, users.email_user, users.pengalaman, users.akun_twitter, tbl_partai.nama_partai FROM users JOIN tbl_partai \
                     WHERE users.partai_id=tbl_partai.partai_id ORDER BY users.created_at DESC")
        data = par.fetchall()
        return data

    def tambahAnggota():
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

    def editAnggota(id):
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

    def semuaPartai():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tbl_partai")
        data = cur.fetchall()
        return data

    def tambahPartai():
        namaPartai = request.form['namaPartai']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_partai WHERE nama_partai = %s", [namaPartai])
        account = cursor.fetchone()
        if account:
            flash(u'Partai sudah terdaftar!', 'danger')
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tbl_partai (nama_partai) VALUES (%s)", [namaPartai])
            mysql.connection.commit()
            flash('Berhasil ditambahkan!', 'success')

    def editPartai(id):
        idu = request.form['idu']
        namePartai = request.form['namePartai']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tbl_partai SET nama_partai = %s WHERE partai_id = %s",
                    (namePartai, idu))
        mysql.connection.commit()
        flash('Data berhasil diubah!', 'success')

    def deleteAnggota(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE user_id=%s", [id])
        mysql.connection.commit()
        flash('Data telah dihapus!', 'danger')

    def deleteAnggotaPartai(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE user_id=%s", [id])
        mysql.connection.commit()

    def deletePartai(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tbl_partai WHERE partai_id=%s", [id])
        mysql.connection.commit()
        flash('Data telah dihapus!', 'danger')