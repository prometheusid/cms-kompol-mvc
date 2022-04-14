import math

def nilai_eigen(criteria, total):
    x = criteria / total
    return x

def eigen_criteria(eigenJmlC1, eigenSentimentC1, eigenEksiC2, eigenCitraC2, eigenJmlC3, eigenSentimentC3, eigenJmlC4, eigenSentimentC4, rataEigenCriteria):
    c1 = (eigenJmlC1 + eigenSentimentC1) * rataEigenCriteria[0]
    c2 = (eigenEksiC2 + eigenCitraC2) * rataEigenCriteria[1]
    c3 = (eigenJmlC3 + eigenSentimentC3) * rataEigenCriteria[2]
    c4 = (eigenJmlC4 + eigenSentimentC4) * rataEigenCriteria[3]
    total = c1 + c2 + c3 + c4
    return [round(c1, 3), round(c2, 3), round(c3, 3), round(c4, 3), round(total, 3)]

    # rata-rata nilai eigen yang sudah ditentukan sebelumnya
    # jml_c1 = 0,8333333333
    # sentiment_c1 = 0,1666666667
    # eksi_c2 = 0,7509398496
    # citra_c2 = 0,2490601504
    # jml_c3 = 0,8753283713
    # sentiment_c3 = 0,1246716287
    # jml_c4 = 0,7509398496
    # sentiment_c4 = 0,2377819549

class Calculate():
    def eigen_partai(data, countData, rataEigenCriteria):

        konsJmlC1 = 0.8333333333
        konsSentimentC1 = 0.1666666667
        konsEksiC2 = 0.7509398496
        konsCitraC2 =  0.2490601504
        konsJmlC3 = 0.8753283713
        konsSentimentC3 = 0.1246716287
        konsJmlC4 = 0.7509398496
        konsSentimentC4 = 0.2490601504

        eigenJmlC1 = []
        eigenSentimentC1 = []
        eigenEksiC2 = []
        eigenCitraC2 = []
        eigenJmlC3 = []
        eigenSentimentC3 = []
        eigenJmlC4 = []
        eigenSentimentC4 = []
        
        nilaiEigenCriteria = []

        for i in range(len(data)):
            eigenJmlC1.append(nilai_eigen(data[i]['komunikator_jumlah'], countData[0]['jml_c1']) * konsJmlC1)
            eigenSentimentC1.append(nilai_eigen(data[i]['komunikator_sentiment'], countData[0]['sentiment_c1']) * konsSentimentC1)
            eigenEksiC2.append(nilai_eigen(data[i]['popularitas_eksistensi'], countData[0]['eksi_c2']) * konsEksiC2)
            eigenCitraC2.append(nilai_eigen(data[i]['popularitas_citra'], countData[0]['citra_c2']) * konsCitraC2)
            eigenJmlC3.append(nilai_eigen(data[i]['laporan_jumlah'], countData[0]['jml_c3']) * konsJmlC3)
            eigenSentimentC3.append(nilai_eigen(data[i]['laporan_sentiment'], countData[0]['sentiment_c3']) * konsSentimentC3)
            eigenJmlC4.append(nilai_eigen(data[i]['integritas_jumlah'], countData[0]['jml_c4']) * konsJmlC4)
            eigenSentimentC4.append(nilai_eigen(data[i]['integritas_sentiment'], countData[0]['sentiment_c4']) * konsSentimentC4)
        
        for i in range(len(data)):
            nilaiEigenCriteria.append({'partai_id' : data[i]['partai_id'], 'nama_partai' : data[i]['nama_partai'], 'value' : eigen_criteria(eigenJmlC1[i], eigenSentimentC1[i], eigenEksiC2[i], eigenCitraC2[i], eigenJmlC3[i], eigenSentimentC3[i], eigenJmlC4[i], eigenSentimentC4[i], rataEigenCriteria)})

        return nilaiEigenCriteria
        