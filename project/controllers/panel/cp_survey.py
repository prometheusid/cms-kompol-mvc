
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
"""
    Import MOdels
from project.models.Hello import Hello
"""
#route index
@app.route("/dashboard/survey/question")
def cp_survey():
    title = ("Data Survey")
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * from tbl_survey_question ORDER BY created_date DESC")
    data = cur.fetchall()
    return render_template('panel/cp_survey/index.html', data=data, title=title)
