from project import app
from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import datetime
from project.config.Database import mysql

# Import models
from project.models.Survey import Survey


#index info
@app.route('/survey-dprd', methods = ['GET'])
def surveyDpr():
    title = ("Survey")
    data = Survey.fetchQuestionDPRD()
    return render_template('public/survey/index.html', data = data, title = title)

