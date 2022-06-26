import math

def nilai_eigen(criteria, total):
    if total != 0:
        x = criteria / total
    else:
        x = 0
    return x

def eigen_criteria(eigenAkademikC1, eigenExperienceC1, eigenEksiC2, eigenCitraC2, eigenJmlC3, eigenSentimentC3, eigenJmlC4, eigenSentimentC4, eigenJmlC5, eigenSentimentC5, rataEigenCriteria):
    c1 = (eigenAkademikC1 + eigenExperienceC1) * rataEigenCriteria[0]
    c2 = (eigenEksiC2 + eigenCitraC2) * rataEigenCriteria[1]
    c3 = (eigenJmlC3 + eigenSentimentC3) * rataEigenCriteria[2]
    c4 = (eigenJmlC4 + eigenSentimentC4) * rataEigenCriteria[3]
    c5 = (eigenJmlC5 + eigenSentimentC5) * rataEigenCriteria[4]
    total = c1 + c2 + c3 + c4 + c5
    return [round(c1, 5), round(c2, 5), round(c3, 5), round(c4, 5), round(c5, 5), round(total, 5)]

class CalculateDewan():
    def eigen_dewan(data, countData, rataEigenCriteria):

        akademikC1 = 0.1666666667
        experienceC1 = 0.8333333333
        eksiC2 = 0.7509398496
        citraC2 =  0.2490601504
        jmlC3 = 0.7509398496
        sentimentC3 = 0.2490601504
        jmlC4 = 0.8753283713
        sentimentC4 = 0.1246716287
        jmlC5 = 0.7509398496
        sentimentC5 = 0.2490601504

        eigenAkademikC1 = []
        eigenExperienceC1 = []
        eigenEksiC2 = []
        eigenCitraC2 = []
        eigenJmlC3 = []
        eigenSentimentC3 = []
        eigenJmlC4 = []
        eigenSentimentC4 = []
        eigenJmlC5 = []
        eigenSentimentC5 = []
        
        nilaiEigenCriteria = []

        for i in range(len(data)):
            eigenAkademikC1.append(nilai_eigen(data[i]['kompetensi_akademik'], countData[0]['kompetensi_c1']) * akademikC1)
            eigenExperienceC1.append(nilai_eigen(data[i]['kompetensi_experience'], countData[0]['experience_c1']) * experienceC1)
            eigenEksiC2.append(nilai_eigen(data[i]['popularitas_eksistensi'], countData[0]['eksi_c2']) * eksiC2)
            eigenCitraC2.append(nilai_eigen(data[i]['popularitas_citra'], countData[0]['citra_c2']) * citraC2)
            eigenJmlC3.append(nilai_eigen(data[i]['forum_jumlah'], countData[0]['jml_c3']) * jmlC3)
            eigenSentimentC3.append(nilai_eigen(data[i]['forum_sentiment'], countData[0]['sentiment_c3']) * sentimentC3)
            eigenJmlC4.append(nilai_eigen(data[i]['laporan_jumlah'], countData[0]['jml_c4']) * jmlC4)
            eigenSentimentC4.append(nilai_eigen(data[i]['laporan_sentiment'], countData[0]['sentiment_c4']) * sentimentC4)
            eigenJmlC5.append(nilai_eigen(data[i]['integritas_jumlah'], countData[0]['jml_c5']) * jmlC5)
            eigenSentimentC5.append(nilai_eigen(data[i]['integritas_sentiment'], countData[0]['sentiment_c5']) * sentimentC5)
        
        for i in range(len(data)):
            nilaiEigenCriteria.append({'id' : data[i]['id'], 'user_id' : data[i]['user_id'], 'name_user' : data[i]['nama_user'],'value' : eigen_criteria( eigenAkademikC1[i], eigenExperienceC1[i], eigenEksiC2[i], eigenCitraC2[i], eigenJmlC3[i], eigenSentimentC3[i], eigenJmlC4[i], eigenSentimentC4[i], eigenJmlC5[i], eigenSentimentC5[i], rataEigenCriteria)})

        return nilaiEigenCriteria