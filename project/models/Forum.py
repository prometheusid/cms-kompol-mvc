from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session, flash
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import os

class Forum:
    def fetchDataForumHome():
        title = ("FORUM DISKUSI")
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * from tbl_forum as a JOIN users as b ON a.user_id = b.user_id WHERE b.user_id ORDER BY a.created_at DESC")
        data = cur.fetchall()
        return data
    
    def fetchCountForumHome():
         # Get Count commentar
        count = mysql.connection.cursor()
        count.execute(
            "SELECT count('forum_id') FROM tbl_forum as a LEFT JOIN tbl_detail_forum as b ON a.forum_id=b.forum_id WHERE a.forum_id=b.id_detail_forum")
        #counting = count.fetchone()
        num_of_items = [v for v in count.fetchone().values()][0]
        
        return num_of_items
   