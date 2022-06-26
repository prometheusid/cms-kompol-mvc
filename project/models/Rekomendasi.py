from project import app
from project.config.Database import mysql
from datetime import datetime
from flask import render_template, redirect, url_for, request, session
from flask_mysqldb import MySQLdb


class Rekomendasi:
    def getHighestScoreAhpPartai(data):
        dataScore = []
        for item in data:
            dataScore.append({'partai_id' : item['partai_id'], 'score' : item['value'][4]});
        newlist = sorted(dataScore, key=lambda k: k['score'], reverse=True)
        return newlist
    
    def getPartaiRekomendasi(listScore):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from rekomendasi_partai")
        datas = cur.fetchall() 

        sortData = []
        for item in listScore: 
            for data in datas:
                if (data['partai_id'] == item['partai_id']):
                    sortData.append({'id': data['id'], 'partai_id' : data['partai_id'], 'judul' : data['judul'], 'content' : data['content'],'images' : data['images'], 'created_at' : data['created_at']});
        
        # mengambil  4 data saja untuk ditampilkan karena sebuah rekomendasi
        rekomendasiData = []
        x = range(4)
        for n in x:
            rekomendasiData.append(sortData[n])
        return rekomendasiData

    def dprdSementara():
        cur = mysql.connection.cursor()
        cur.execute(
        "SELECT * from rekomendasi_dewan ORDER BY id")
        data = cur.fetchall()

        rekomendasiData = []
        x = range(4)
        for n in x:
            rekomendasiData.append(data[n])
        return rekomendasiData

    def detail(id):
        cur = mysql.connection.cursor()
        cur.execute(
        "SELECT * from rekomendasi_partai WHERE id=%s", (id,))
        data = cur.fetchone()
        return data
    
    def detailDewan(id):
        cur = mysql.connection.cursor()
        cur.execute(
        "SELECT * from rekomendasi_dewan WHERE id=%s", (id,))
        data = cur.fetchone()
        return data