
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime

# Import models
from project.models.Survey import Survey

#route index
@app.route("/dashboard/survey/question")
def cp_survey():
    title = ("Data Survey")
    # fetch data from model
    data = Survey.fetchQuestion()
    return render_template('panel/cp_survey/index.html', data=data, title=title)
