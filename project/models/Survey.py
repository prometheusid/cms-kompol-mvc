from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session

class Survey:
    
    def fetchQuestion():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from tbl_survey_question ORDER BY created_date DESC")
        data = cur.fetchall()
        return data

    def addDataQuestion():
        code = request.form['code']
        question = request.form['question']
        variabel = request.form['variabel']
        created_date = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `tbl_survey_question` (`id_survey_question`, `code`, `question`, `variabel`, `created_date`) VALUES (%s,%s,%s,%s,%s)",
                    ('Null', code, question, variabel, created_date))
        mysql.connection.commit()