
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

# generate random integer values
from random import seed
from random import randint

# Import models
from project.models.Survey import Survey

#route index
@app.route("/dashboard/survey/question")
def cp_survey():
    title = ("Data Survey")
    # fetch data from model
    value = "q"+str(randint(0, 999))
    data = Survey.fetchQuestion()
    return render_template('panel/cp_survey/index.html', data=data, value=value, title=title)

@app.route("/survey/tambah-question", methods=["GET", "POST"])
def cp_survey_question():
    data = Survey.addDataQuestion()
    return redirect(url_for('cp_survey'))
