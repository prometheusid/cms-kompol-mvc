
from project import app
from flask import render_template, redirect, url_for, request, session, flash
from datetime import datetime
from project.config.Database import mysql
from flask_mysqldb import MySQLdb
import bcrypt
from bcrypt import hashpw
from project.models.Encryption import Encryption
import re

#route index
@app.route("/registrasi", methods=["GET", "POST"])
def registrasi():
    if request.method == 'GET':
        return render_template('auth/registrasi.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        validatePassword = request.form['validate_password']

        if (password != validatePassword):
            flash('Gagal, Password yang anda masukkan tidak sesuai')
            return render_template('auth/registrasi.html', response="error")

        checkEmail = Encryption.checkEmail(email)
        if (checkEmail == True):
            flash('Gagal, Email sudah dipakai')
            return render_template('auth/registrasi.html', response="error")
        
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
            return render_template('auth/registrasi.html', response="error")
        elif not re.match(r'[A-Za-z0-9]+', name):
            flash('Name must contain only characters!')
            return render_template('auth/registrasi.html', response="error")
        elif not name or not password or not email:
            flash('Please fill out the form!')
            return render_template('auth/registrasi.html', response="error")
        else:
            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            role_id = 4
            partai_id = 0
            created = datetime.now()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (nama_user, email_user, password, role_id, partai_id, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (name, email, hash_password, role_id, partai_id, created, created))
            mysql.connection.commit()
            cur.close()

            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        #password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email_user = %s", (email,))
        user = curl.fetchone()
        curl.close()

        if user:
            session['loggedin'] = True
            session['id'] = user['user_id']
            session['name'] = user['nama_user']
            session['email'] = user['email_user']
            session['role'] = user['role_id']
                #login_user(user)
            return redirect(url_for('pub_home'))
        else:
            msg = 'Incorrect username / password !'
    return render_template("auth/login.html", msg=msg)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('pub_home'))