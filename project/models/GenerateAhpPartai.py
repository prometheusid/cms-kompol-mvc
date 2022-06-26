import re
from project.config.Database import mysql
from datetime import datetime

from project.models.Crawling import Crawling
from project.models.Sentiment import Sentiment

from operator import itemgetter
from itertools import groupby
from functools import partial

class GenerateAhpPartai:
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
            value = (komunikatorJumlah, pointKomunikatorSentiment, updatedAt, item['partai_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()

        return "berhasil"
    
    def updateIntegritas():
        tweetIntegritas = Crawling.getTweetIntegritasPartai()
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

        return "berhasil"
    
    def updateSentimentLapkun():
        connect = mysql.connection.cursor()
        connect.execute("SELECT A.lapkun_id, A.user_id, B.komentar as tweet, C.partai_id FROM tbl_lapkun as A JOIN tbl_detail_lapkun as B ON A.lapkun_id = B.lapkun_id JOIN users as C ON A.user_id = C.user_id")
        lapkun = connect.fetchall()
      
        data = Sentiment.predictLapkun(lapkun)

        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in data:
            laporanSentiment = (item['total_positive'] / (item['total_positive'] + item['total_negative'])) * 100
            pointLaporanSentiment = GenerateAhpPartai.valueSentiment(laporanSentiment)

            sql_update = "UPDATE tbl_ahp_partai SET laporan_sentiment = %s, updated_at = %s WHERE partai_id = %s"
            value = (pointLaporanSentiment, updatedAt, item['partai_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()

        return "berhasil"
    
    def updateJumlahLapkun():
        connect = mysql.connection.cursor()
        connect.execute("SELECT COUNT(A.lapkun_id) as jumlah,B.partai_id FROM tbl_lapkun as A JOIN users as B ON A.user_id = B.user_id GROUP BY B.partai_id")
        lapkun = connect.fetchall() 

        updatedAt = datetime.now()
        update = mysql.connection.cursor()
        for item in lapkun:
            sql_update = "UPDATE tbl_ahp_partai SET laporan_jumlah = %s, updated_at = %s WHERE partai_id = %s"
            value = (item['jumlah'], updatedAt, item['partai_id'])
            update.execute(sql_update, value)
        mysql.connection.commit()

        return "berhasil"
    
    def updateSurvey():
        connect = mysql.connection.cursor()
        connect.execute("SELECT A.id_partai, A.code_answer, B.id_survey_question, B.answer FROM tbl_survey_partai as A RIGHT JOIN tbl_survey_answer_partai as B ON A.code_answer = B.code_answer")
        survey = connect.fetchall() 

        groupCodeAnswers = dict(map(lambda k_v: (k_v[0], tuple(map(partial(GenerateAhpPartai.del_ret, key="code_answer"), k_v[1]))),groupby(survey, itemgetter("code_answer"))))

        groups = []
        for k, v in groupCodeAnswers.items():
            groups.append({"code_answer" : k, "value" : v})
        
        test = []
        for i in range(0, len(groups)):
            pointCitra = 0
            pointEksistensi = 0
            for j in range(0, len(groups[i]['value'])):
                if (groups[i]['value'][j]['id_survey_question'] == 20 or groups[i]['value'][j]['id_survey_question'] == 20):
                    pointCitra  += int(groups[i]['value'][j]['answer'])
            test.append({"partai_id" : groups[i]['value'][0]['id_partai'], "point_citra" : pointCitra })


        return test
    
    def del_ret(d, key):
        del d[key]
        return d
