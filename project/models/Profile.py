import os
from project import app
from project.config.Database import mysql
from datetime import datetime
from os.path import join, dirname, realpath
from flask import render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQLdb
from werkzeug.utils import secure_filename

# generate random integer values
from random import seed
from random import randint

class Profile:

    UPLOAD_FOLDER = join(dirname(realpath(__file__)), '../uploadedFiles/users')

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def allowed_file(filename):
        return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Profile.ALLOWED_EXTENSIONS

    def updateImage(id):
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and Profile.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET images = %s WHERE user_id = %s",
                    (filename, id))
        mysql.connection.commit()

    def detaiilProfile(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users JOIN role_users ON role_users.role_id=users.role_id \
                    JOIN tbl_partai ON tbl_partai.partai_id=users.partai_id WHERE users.user_id=%s", (id,))
        profiles = cur.fetchone()
        return profiles

    def detailProfile(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users JOIN role_users ON role_users.role_id=users.role_id \
                    WHERE users.user_id=%s", (id,))
        profileu = cur.fetchone()
        return profileu

    def editProfiles(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users JOIN role_users ON role_users.role_id=users.role_id \
                    LEFT JOIN tbl_partai ON tbl_partai.partai_id=users.partai_id \
                    WHERE users.user_id=%s", (id,))
        profile = cur.fetchone()
        return profile
    
    def eduProfile(id):
        edu = mysql.connection.cursor()
        edu.execute("SELECT * FROM users JOIN tbl_pendidikan ON tbl_pendidikan.id_pendidikan=users.id_pendidikan WHERE users.user_id=%s", (id,))
        edu = edu.fetchone()
        return edu

    def ahpPartai(id):
        ahp = mysql.connection.cursor()
        ahp.execute("SELECT * FROM users as A JOIN tbl_ahp_partai as B ON a.partai_id = B.partai_id WHERE a.user_id=%s", (id,))
        ahp = ahp.fetchone()
        return ahp

    def listPengalaman(id):
        experiences = mysql.connection.cursor()
        experiences.execute("SELECT id, user_id, pengalaman FROM tbl_pengalaman WHERE user_id = %s", [id])
        experiences = experiences.fetchall()
        return experiences 