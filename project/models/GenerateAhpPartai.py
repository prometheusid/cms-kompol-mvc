from project.config.Database import mysql
from datetime import datetime

from project.models.Crawling import Crawling
from project.models.Sentiment import Sentiment
# TODO : Tinggal update laporan karan survei sudah beres sama raka
class GenerateAhpPartai:
    def updateAhpPartai():
        GenerateAhpPartai.updateIntegritas
        GenerateAhpPartai.updateKomunikator
        GenerateAhpPartai.updateLapkun
        return "berhasil"
        
    def valueSentiment(value):
        if (value >= 90):
            point = 100
        if (value >= 85 and value <= 89):
            point = 95
        if (value >= 80 and value <= 84):
            point = 90  
        if (value >= 70 and value <= 79):
            point = 85 
        if (value >= 60 and value <= 69):
            point = 80 
        if (value >= 55 and value <= 59):
            point = 75
        if (value >= 50 and value <= 54):
            point = 70
        if (value >= 40 and value <= 49):
            point = 60 
        if (value >= 30 and value <= 39):
            point = 55  
        if (value >= 20 and value <= 29):
            point = 50
        if (value >= 10 and value <= 19):
            point = 40
        if (value >= 0 and value <= 9):
            point = 30
        return point

    def updateKomunikator():
        tweetKomunikator = Crawling.getTweetKomunikatorPartai()
        sentimentKomunikator = Sentiment.predictPartai(tweetKomunikator)
       
        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in sentimentKomunikator:
            komunikatorJumlah = item['total_positive'] + item['total_negative']
            komunikatorSentiment = (item['total_positive'] / (item['total_positive'] + item['total_negative'])) * 100
            pointKomunikatorSentiment = GenerateAhpPartai.valueSentiment(komunikatorSentiment)

            sql_update = "UPDATE tbl_ahp_partai SET komunikator_jumlah = %s, komunikator_sentiment = %s, updated_at = %s WHERE partai_id = %s"
            value = (komunikatorJumlah, pointKomunikatorSentiment,updatedAt, item['partai_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()
    
    def updateIntegritas():
        tweetIntegritas = Crawling.getTweetKomunikatorPartai()
        sentimentIntegritas = Sentiment.predictPartai(tweetIntegritas)
       
        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in sentimentIntegritas:
            integritasJumlah = item['total_positive'] + item['total_negative']
            integritasSentiment = (item['total_positive'] / (item['total_positive'] + item['total_negative'])) * 100
            pointIntegritasSentiment = GenerateAhpPartai.valueSentiment(integritasSentiment)

            sql_update = "UPDATE tbl_ahp_partai SET integritas_jumlah = %s, integritas_sentiment = %s, updated_at = %s WHERE partai_id = %s"
            value = (integritasJumlah, pointIntegritasSentiment ,updatedAt, item['partai_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()
    
    def updateLapkun():
        cur = mysql.connection.cursor()
        cur.execute("SELECT b.partai_id, count(b.partai_id) as jumlah from tbl_lapkun as a Join users as b on a.user_id = b.user_id GROUP BY b.partai_id")
        data = cur.fetchall()
        return data