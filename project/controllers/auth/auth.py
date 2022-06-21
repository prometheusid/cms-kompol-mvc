
from project import app
from flask import render_template, redirect, url_for, request, session, flash
from datetime import datetime
from project.config.Database import mysql
from flask_mysqldb import MySQLdb
import bcrypt
from bcrypt import hashpw

#route index
@app.route("/registrasi", methods=["GET", "POST"])
def registrasi():
    if request.method == 'GET':
        return render_template('auth/registrasi.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        role_id = 4
        partai = 0
        created = datetime.now()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (nama_user, email_user, password, role_id, partai_id, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
                    (name, email, hash_password, role_id, partai, created))
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