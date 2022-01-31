
from ast import dump
from project import app
from flask import render_template, redirect, url_for, request, session, make_response
from datetime import datetime
from project.config.Database import mysql
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
"""
    Import MOdels
from project.models.Hello import Hello
"""
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

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (nama_user, email_user, password) VALUES (%s,%s,%s)",
                    (name, email, hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('pub_home'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email_user=%s", (email,))
        user = curl.fetchone()
        # dump(user)
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['id'] = user['user_id']
                session['name'] = user['nama_user']
                session['email'] = user['email_user']
                session['role'] = user['role_id']
                # return render_template("/public/index.html")
                if user['role_id'] == 0:
                    return redirect(url_for('cp_survey'))
                elif user['role_id'] == 1:
                    return redirect(url_for('pub_home'))

            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("auth/login.html")


@app.route('/logout')
def logout():
    session.clear()
    # return render_template("/public/index.html")
    return redirect(url_for('pub_home'))