import math


def aksen(nilai):
    if nilai < 1:
        x = round(1/nilai)
    else:
        x = round(1/nilai, 2)
    return x


def nilai_eigen(criteria, total):
    x = criteria / total
    return x


def sum_avg_eigen(jumlah, n):
    x = jumlah / n
    return x

# TODO : bisa dicari untuk ri berapa2nya


class Criteria():
    def perbandingan(value, n):
        data = {}
        criteria = []
        eigen = []
        rata_eigen = []

        # Untuk AHP Partai
        if n == 4:
            name_criteria = ['Komunikator Politik',
                             'Popularitas', 'Akuntabilitas', 'Integritas']

        # Untuk AHP Dewan
        if n == 5:
            name_criteria = ['Komunikator Politik',
                             'Popularitas', 'Akuntabilitas', 'Integritas']

        # Masukan criteria ke dalam matrix perbadingan
        temp = 0
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(1)
                elif j > i:
                    row.append(float(value[temp]))
                    temp = temp + 1
                else:
                    row.append(aksen(criteria[j][i]))
            criteria.append(row)
        # Total criteria per row
        total_criteria = [sum(x) for x in zip(*criteria)]
        # Matrix Eigen
        for i in range(n):
            temp = []
            for j in range(n):
                temp.append(nilai_eigen(criteria[i][j], total_criteria[j]))
            eigen.append(temp)
        # Row Eigen
        jumlah_eigen = list(map(sum, eigen))
        # Row Rata-rata Eigen
        for i in range(n):
            rata_eigen.append(sum_avg_eigen(jumlah_eigen[i], n))
        # Cek eigen apakah 1 jika sesuai berarti benar
        cek_eigen = sum(map(lambda x: x, rata_eigen))
        # Menghitung lambda
        lambda_max = sum(map(lambda x, y: x * y, total_criteria, rata_eigen))
        # Menghitunf consistensi index
        ci = (lambda_max - n) / (n-1)
        # TODO : cari jika n = 4 atau n = 5 bisa disesuaikan dengan menggunakan (IF Statement)
        ri = 0.9
        # Menghitung Rasio Index
        cr = ci / ri

        data['name_criteria'] = name_criteria
        data['criteria'] = criteria
        data['total_criteria'] = total_criteria
        data['eigen'] = eigen
        data['jumlah_eigen'] = jumlah_eigen
        data['rata_eigen'] = rata_eigen
        data['cek_eigen'] = cek_eigen
        data['lambda_max'] = lambda_max
        data['ci'] = ci
        data['cr'] = cr

        return data
