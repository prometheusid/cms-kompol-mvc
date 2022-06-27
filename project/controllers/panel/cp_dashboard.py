from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
"""
    Import MOdels
from project.models.Hello import Hello
"""

# Import Model
from project.models.Dashboard import Dashboard
from project.models.Survey import Survey

# dashboard / cpanel admin
@app.route("/dashboard/<id>")
def dashboard(id):
    user = Dashboard.getUsers(id)
    countDprd = Dashboard.countDprd()
    countPartai = Dashboard.countPartai()
   
    countWarga = Dashboard.countWarga()
    countInfo = Dashboard.countInfo()
    countSurveyPartai = Survey.countSurveyPartai()
    countSurveyDprd = Survey.countSurveyDPRD()
    return render_template('panel/cp_dashboard/index.html', user=user, countSurveyPartai=countSurveyPartai, countSurveyDprd=countSurveyDprd, countDprd=countDprd, countInfo=countInfo, countPartai=countPartai, countWarga=countWarga)