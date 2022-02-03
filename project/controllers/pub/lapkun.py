from flask import render_template
from project import app
from project.config.Database import mysql
from datetime import datetime
"""
    Import MOdels
from project.models.Hello import Hello
"""

#route index
@app.route("/lapkun")
def lapkun():
    return render_template('/public/lapkun/index.html')