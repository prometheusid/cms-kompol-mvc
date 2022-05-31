from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session, flash
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQLdb
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

    def tambahForum():
        # idForum = request.form['idForum']
        judulForum = request.form['judulForum']
        isi = request.form['content']
        ts = session['id']
        author = 'Author'
        waktu = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_forum (forum_judul, forum_isi, user_id, author, created_at) VALUES (%s,%s,%s,%s,%s)",
                    (judulForum, isi, ts, author, waktu))
              
        if session['role'] == 2:
            curl_users = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl_users.execute("SELECT * FROM users WHERE user_id = %s", (ts,))
            data_users= curl_users.fetchone()
            curl_users.close()

            id_partai = data_users['partai_id']

            curl_ahp_partai = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl_ahp_partai.execute("SELECT * FROM tbl_ahp_partai WHERE partai_id = %s", (id_partai,))
            ahp_partai = curl_ahp_partai.fetchone()
            curl_ahp_partai.close()

            ahp_eksistensi_before = ahp_partai['popularitas_eksistensi']
            ahp_eksistensi = int(ahp_eksistensi_before) + 15

            update = mysql.connection.cursor()
            sql_update = "UPDATE tbl_ahp_partai SET popularitas_eksistensi = %s WHERE partai_id = %s"
            value_ahp = (ahp_eksistensi, id_partai)
            update.execute(sql_update, value_ahp)

        if session['role'] == 3:
            user_id = session['id']

            curl_ahp_dprd = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl_ahp_dprd.execute("SELECT * FROM tbl_ahp_dprd WHERE user_id = %s", (user_id,))
            ahp_dprd = curl_ahp_dprd.fetchone()
            curl_ahp_dprd.close()

            ahp_eksistensi_before = ahp_dprd['popularitas_eksistensi']
            ahp_eksistensi = int(ahp_eksistensi_before) + 15

            ahp_forum_jumlah_before = ahp_dprd['forum_jumlah']
            ahp_forum_jumlah = int(ahp_forum_jumlah_before) + 10

            ahp_forum_sentiment_before = ahp_dprd['forum_sentiment']
            ahp_forum_sentiment = int(ahp_forum_sentiment_before) + 10

            update = mysql.connection.cursor()
            sql_update = "UPDATE tbl_ahp_dprd SET popularitas_eksistensi = %s, forum_jumlah = %s, forum_sentiment = %s WHERE user_id = %s"
            value_ahp = (ahp_eksistensi, ahp_forum_jumlah, ahp_forum_sentiment, user_id)
            update.execute(sql_update, value_ahp)
        
        mysql.connection.commit()

    def komentarForum():
        idForum = request.form['idForum']
        komen = request.form['komen']
        komenUser = session['id']
        waktu = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_detail_forum (forum_id, komentar, user_id, created_at) VALUES (%s,%s,%s,%s)",
                    (idForum, komen, komenUser, waktu))
        
        if session['role'] == 2:
            curl_users = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl_users.execute("SELECT * FROM users WHERE user_id = %s", (komenUser,))
            data_users= curl_users.fetchone()
            curl_users.close()

            id_partai = data_users['partai_id']

            curl_ahp_partai = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl_ahp_partai.execute("SELECT * FROM tbl_ahp_partai WHERE partai_id = %s", (id_partai,))
            ahp_partai = curl_ahp_partai.fetchone()
            curl_ahp_partai.close()

            ahp_citra_before = ahp_partai['popularitas_citra']
            ahp_citra = int(ahp_citra_before) + 10

            update = mysql.connection.cursor()
            sql_update = "UPDATE tbl_ahp_partai SET popularitas_citra = %s WHERE partai_id = %s"
            value_ahp = (ahp_citra, id_partai)
            update.execute(sql_update, value_ahp)

        if session['role'] == 3:
            user_id = session['id']

            curl_ahp_dewan = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl_ahp_dewan.execute("SELECT * FROM tbl_ahp_dprd WHERE user_id = %s", (user_id,))
            ahp_dewan = curl_ahp_dewan.fetchone()
            curl_ahp_dewan.close()

            ahp_citra_before = ahp_dewan['popularitas_citra']
            ahp_citra = int(ahp_citra_before) + 10

            ahp_forum_jumlah_before = ahp_dewan['forum_jumlah']
            ahp_forum_jumlah = int(ahp_forum_jumlah_before) + 5

            ahp_forum_sentiment_before = ahp_dewan['forum_sentiment']
            ahp_forum_sentiment = int(ahp_forum_sentiment_before) + 10

            update = mysql.connection.cursor()
            sql_update = "UPDATE tbl_ahp_dprd SET popularitas_citra = %s, forum_jumlah = %s, forum_sentiment = %s WHERE user_id = %s"
            value_ahp = (ahp_citra, ahp_forum_jumlah, ahp_forum_sentiment, user_id)
            update.execute(sql_update, value_ahp)
        mysql.connection.commit()

    def replyKomentar():
        idForum = request.form['idForum']
        idKomen = request.form['idKomen']
        idReply = request.form['idReply']
        replyUser = session['id']
        replykomen = request.form['replykomen']
        waktu = datetime.now()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_reply_komen (reply_id, forum_id, id_detail_forum, user_id, reply_komen, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
                    (idForum, idKomen, idReply, replyUser, replykomen, waktu))


        
   