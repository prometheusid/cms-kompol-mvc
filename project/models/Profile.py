from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session
from flask_mysqldb import MySQLdb

# generate random integer values
from random import seed
from random import randint

class Profile:

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