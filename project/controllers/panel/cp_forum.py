
import imp
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import mysql
from datetime import datetime
# Import Model
from project.models.Forum import Forum

@app.route("/dashboard/cp_forum")
def cp_forum():
    title = ('FORUM')
    data = Forum.fetchDataForumHome()
    return render_template('panel/cp_forum/index.html', data=data, title=title)


@app.route("/dashboard/cp_forum/delete/<int:id>")
def hapus_forum(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tbl_forum WHERE forum_id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('cp_forum'))