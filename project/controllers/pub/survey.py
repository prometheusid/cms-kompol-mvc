from project import app
from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import datetime
from project.config.Database import mysql

# Import models
from project.models.Survey import Survey


#index info
@app.route('/surveys', methods = ['GET'])
def surveys():
    title = ("Survey")
    data = Survey.fetchQuestionDPRD()
    return render_template('public/survey/index.html', data = data, title = title)

@app.route('/survey-dprd', methods = ['GET'])
def surveyDpr():
    title = ("Survey DPRD")
    data = Survey.fetchQuestionDPRD()
    return render_template('public/survey/dprd.html', data = data, title = title)

@app.route('/survey-partai', methods = ['GET'])
def surveyPartai():
    title = ("Survey Partai")
    data = Survey.fetchQuestionPartai()
    return render_template('public/survey/partai.html', data = data, title = title)

@app.route('/surveys/save', methods = ['POST'])
def saveSurveyDpr():
    title = ("Survey DPRD")
    data = Survey.fetchQuestionDPRD()
    jumlah = len(data)
    for i in range(1, jumlah):
        id_question = request.form['id_question'+str(i)]
        jawaban = request.form.getlist('row'+str(i))
        return render_template('public/survey/index2.html', data = data, title = title, hasil=id_question, jawaban=i)
