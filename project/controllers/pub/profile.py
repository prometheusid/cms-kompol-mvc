from ast import dump
from project import app
from flask import render_template, redirect, url_for, request, session, make_response
from datetime import datetime
from project.config.Database import mysql
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

@app.route("/profile/<id>")
def profileuser(id):
    title = ("PROFILE")
    profile = mysql.connection.cursor()
    profile.execute("SELECT * FROM users JOIN role_users ON role_users.role_id=users.role_id \
                 JOIN tbl_partai ON tbl_partai.partai_id=users.partai_id \
                 JOIN tbl_pendidikan ON tbl_Pendidikan.id_pendidikan=users.id_pendidikan WHERE users.user_id=%s", (id,))
    profile = profile.fetchone()

    """ adm = mysql.connection.cursor()
    adm.execute("SELECT * FROM users WHERE role_id=1")
    adm = adm.fetchone() """

    return render_template('public/profile/index.html', title=title, profile=profile)

@app.route("/profile/edit/<id>", methods=["GET", "POST"])
def profileedit(id):
    title = ("EDIT PROFILE")
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users JOIN role_users ON role_users.role_id=users.role_id \
                    JOIN tbl_partai ON tbl_partai.partai_id=users.partai_id WHERE user_id=%s", (id,))
        profile = cur.fetchone()

        edu = mysql.connection.cursor()
        edu.execute("SELECT * FROM tbl_pendidikan")
        edu = edu.fetchall()
        return render_template('public/profile/editprofile.html', edu=edu, profile=profile, title=title)
    else:
        idu = request.form['idu']
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        update = datetime.now()
        education = request.form['education']
        pengalaman = request.form['pengalaman']
        twitter = request.form['twitter']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET nama_user = %s, password = %s, updated_at = %s, id_pendidikan = %s, pengalaman = %s, akun_twitter = %s WHERE user_id = %s",
                    (name, hash_password, update, education, pengalaman, twitter, idu))
        mysql.connection.commit()
    return redirect(url_for('profileuser', id=id))