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

# GET data from DPRD
@app.route('/survey-dprd', methods = ['GET'])
def surveyDpr():
    title = ("Survey DPRD")
    data = Survey.fetchQuestionDPRD()
    select = Survey.fetchDataDPRD()
    return render_template('public/survey/dprd.html', data = data, title = title, select = select)

# GET data from question
@app.route('/survey-partai', methods = ['GET'])
def surveyPartai():
    title = ("Survey Partai")
    data = Survey.fetchQuestionPartai()
    select = Survey.fetchDataPartai()
    return render_template('public/survey/partai.html', data = data, title = title, select = select)

# SAVE DPRD
@app.route('/surveys/dprd/save', methods = ['POST'])
def saveSurveyDpr():
    title = ("Survey DPRD")
    check = Survey.checkSurveyDprd()
    if (check == True):
        flash('Gagal, Anda sudah mengisi data sebelumnya')
        return redirect(url_for('surveys'))
    data = Survey.saveDPRDSurvey()
    return redirect(url_for('surveys', title=title))

# SAVE partai
@app.route('/surveys/partai/save', methods = ['POST'])
def saveSurveyPartai():
    title = ("Survey Partai")
    check = Survey.checkSurveyPartai()
    if (check == True):
        flash('Gagal, Anda sudah mengisi data sebelumnya')
        return redirect(url_for('surveyPartai'))
    data = Survey.savePartaiSurvey()
    return redirect(url_for('surveys', title=title))
