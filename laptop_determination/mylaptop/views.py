from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import models

# Create your views here.
def alternatif(request):
    data = models.Laptops.objects.all()
    context = {
        'laptops': data,
    }
    return render(request, 'mylaptop/alternatif.html', context)

def cari(request):
    data = models.Laptops.objects.all()
    criterions = ['Default','Harga','RAM','CPU','SSD','HDD']
    unique_brands = []
    brands = []
    for x in data:
        # check if exists in unique_brands or not
        if x.company not in brands:
            unique_brands.append(x)
            brands.append(x.company)

    context = {
        'brands': unique_brands,
        'criterias':criterions,
        'cari': data
    }

    return render(request, 'mylaptop/cari.html', context)

def hasil(request):
    default = ['HARGA','RAM','SSD','HDD','CPU']
    data = {}
    if request.method == 'POST':
        data['brand'] = request.POST['brand']
        for i in range(5):
            if(request.POST['penting_'+str(i+1)]=='kosong'):
                data['penting'+str(i+1)] = default[i]
            else:
                data['penting'+str(i+1)] = request.POST['penting_'+str(i+1)]

        data_alternatif = models.Laptops.objects.all()
        context = {
            'cari': data,
            'alternatif' : data_alternatif
        }

        context = process(context)

        return render(request, 'mylaptop/hasil.html', context)

    else:
        return HttpResponseRedirect('/mylaptop/cari/')
        # return render(request, 'mylaptop/hasil.html')

def process(context):
    data_pilihan = context.get("cari")
    data_temp = context.get("alternatif")
    data_brand = []
    data_fix = []

    # ambil data yang sesuai brand
    if data_pilihan['brand'] != 'Semua':
        for data in data_temp:
            if data.company == data_pilihan['brand']:
                data_brand.append(data)

    # ambil data jika tidak ada pilihan brand
    else:
        for data in data_temp:
            data_brand.append(data)

    # n = len(data_brand)
    n = 5

    # ambil n data awal dan tambahkan nilai default 0
    for i in range(n):
        data_fix.append({"obj":data_brand[i],"cpu":{"awal":[0]*n, 
                                                    "normalisasi":[0]*n, 
                                                    "weight":0, 
                                                    "terbobot":[0]*n,
                                                    "wsv":0,
                                                    "cv":0,
                                                    "lambda_max":0.0,
                                                    "ci":0,
                                                    "cr":0
                                                    },
                                            "harga":{"awal":[0]*n, 
                                                    "normalisasi":[0]*n, 
                                                    "weight":0, 
                                                    "terbobot":[0]*n,
                                                    "wsv":0,
                                                    "cv":0,
                                                    "lambda_max":0.0,
                                                    "ci":0,
                                                    "cr":0
                                                    },
                                            "ram":{"awal":[0]*n, 
                                                    "normalisasi":[0]*n, 
                                                    "weight":0, 
                                                    "terbobot":[0]*n,
                                                    "wsv":0,
                                                    "cv":0,
                                                    "lambda_max":0.0,
                                                    "ci":0,
                                                    "cr":0
                                                    },
                                            "ssd":{"awal":[0]*n, 
                                                    "normalisasi":[0]*n, 
                                                    "weight":0, 
                                                    "terbobot":[0]*n,
                                                    "wsv":0,
                                                    "cv":0,
                                                    "lambda_max":0.0,
                                                    "ci":0,
                                                    "cr":0
                                                    },
                                            "hdd":{"awal":[0]*n, 
                                                    "normalisasi":[0]*n, 
                                                    "weight":0, 
                                                    "terbobot":[0]*n,
                                                    "wsv":0,
                                                    "cv":0,
                                                    "lambda_max":0.0,
                                                    "ci":0,
                                                    "cr":0
                                            }})

    data_fix = hitungAlternatif(data_fix.copy(), "cpu", n)
    data_fix = hitungAlternatif(data_fix.copy(), "harga", n)
    data_fix = hitungAlternatif(data_fix.copy(), "ram", n)
    data_fix = hitungAlternatif(data_fix.copy(), "ssd", n)
    data_fix = hitungAlternatif(data_fix.copy(), "hdd", n)

    # ambil data pilihan (kriteria) lalu di ubah ke bentuk yang sama seperti data alternatif
    data_pilihan_temp = data_pilihan.copy()
    pilihan = []
    for i in range(5):
        pilihan.append(data_pilihan_temp['penting'+str(i+1)])

    data_pilihan = []
    for i in range(5):
        data_pilihan.append({"obj":{"pilihan":pilihan[i]}, "cpu":{"awal":[0]*n, 
                                                            "normalisasi":[0]*n, 
                                                            "weight":0, 
                                                            "terbobot":[0]*n,
                                                            "wsv":0,
                                                            "cv":0,
                                                            "lambda_max":0.0,
                                                            "ci":0,
                                                            "cr":0
                                                            },
                                                    "harga":{"awal":[0]*n, 
                                                            "normalisasi":[0]*n, 
                                                            "weight":0, 
                                                            "terbobot":[0]*n,
                                                            "wsv":0,
                                                            "cv":0,
                                                            "lambda_max":0.0,
                                                            "ci":0,
                                                            "cr":0
                                                            },
                                                    "ram":{"awal":[0]*n, 
                                                            "normalisasi":[0]*n, 
                                                            "weight":0, 
                                                            "terbobot":[0]*n,
                                                            "wsv":0,
                                                            "cv":0,
                                                            "lambda_max":0.0,
                                                            "ci":0,
                                                            "cr":0
                                                            },
                                                    "ssd":{"awal":[0]*n, 
                                                            "normalisasi":[0]*n, 
                                                            "weight":0, 
                                                            "terbobot":[0]*n,
                                                            "wsv":0,
                                                            "cv":0,
                                                            "lambda_max":0.0,
                                                            "ci":0,
                                                            "cr":0
                                                            },
                                                    "hdd":{"awal":[0]*n, 
                                                            "normalisasi":[0]*n, 
                                                            "weight":0, 
                                                            "terbobot":[0]*n,
                                                            "wsv":0,
                                                            "cv":0,
                                                            "lambda_max":0.0,
                                                            "ci":0,
                                                            "cr":0
                                                    }})

    data_pilihan = hitungKriteria(data_pilihan.copy())

    # kumpulkan setiap bobot
    hasil_rangking = []
    for i in range(5):
        hasil_rangking.append({"weight":{pilihan[i].lower():[0]*n}, "pilihan":pilihan[i], "bobot":0})

    for i in range(5):
        hasil_rangking[i]["bobot"] = data_pilihan[i][pilihan[i].lower()]['weight']
        for j in range(n):
            hasil_rangking[i]["weight"][pilihan[i].lower()][j] = data_fix[j][pilihan[i].lower()]['weight']

    # hitung perangkingan
    jumlah = []
    for i in range(n):
        jumlah_temp_alt = 0
        jumlah_temp_kriteria = 0
        for j in range(5):
            jumlah_temp_kriteria += hasil_rangking[j]["bobot"]
            jumlah_temp_alt += hasil_rangking[j]["weight"][pilihan[j].lower()][i]
        jumlah.append(jumlah_temp_alt*jumlah_temp_kriteria)

    hasil_rangking_alternatif = []
    for i in range(n):
        hasil_rangking_alternatif.append({"rangking":jumlah[i], "rank":0, "obj":None})

    # rangking setiap hasil perangkingan
    jumlah = sorted(jumlah, reverse=True)
    i = 1
    for i in range(n):
        hasil_rangking_alternatif[i]['rank'] = jumlah.index(hasil_rangking_alternatif[i]['rangking']) + 1
        hasil_rangking_alternatif[i]['obj'] = data_brand[i]

    context = {
        'cari': data_pilihan,
        'alternatif' : data_fix,
        "rangking" : hasil_rangking,
        "rangking_alternatif" : hasil_rangking_alternatif
    }
    
    return context

def hitungAlternatif(alternatif, kriteria, n):

    # tambahkan kepentingan alternatif yang sama menjadi 1
    i = 0
    for data in alternatif:
        data[kriteria]["awal"][i] = 1
        i += 1

    # tambahkan kepentingan alternatif
    k = n-1
    batas_l = 0
    for i in range(n):
        l = batas_l + 1
        for j in range(k):
            alternatif[i][kriteria]["awal"][l] = 2
            alternatif[l][kriteria]["awal"][i] = 1/2
            l += 1
        batas_l += 1
        k -= 1

    jumlah = []
    # hitung jumlah tiap baris alternatif
    for data in alternatif:
        jumlah_temp = 0
        for i in range(n):
            jumlah_temp += data[kriteria]["awal"][i]
        jumlah.append(jumlah_temp)

    # hitung normalisasi matriks alternatif
    for data in alternatif:
        for i in range(n):
            data[kriteria]["normalisasi"][i] = data[kriteria]["awal"][i]/jumlah[i]

    # hitung weight alternatif
    for data in alternatif:
        weight_temp = 0
        for i in range(n):
            weight_temp += data[kriteria]["normalisasi"][i]
        data[kriteria]["weight"] = weight_temp/n

    # hitung matriks terbobot alternatif
    for data in alternatif:
        for i in range(n):
            data[kriteria]["terbobot"][i] = data[kriteria]["awal"][i]*data[kriteria]["weight"]

    # hitung wsv alternatif
    for data in alternatif:
        data[kriteria]["wsv"] = sum(data[kriteria]["terbobot"])

    # hitung cv alternatif
    for data in alternatif:
        data[kriteria]["cv"] = data[kriteria]["wsv"]/data[kriteria]["weight"]

    # hitung lambda_max alternatif
    lambda_temp = 0
    for data in alternatif:
        lambda_temp += data[kriteria]["cv"]
    for data in alternatif:
        data[kriteria]["lambda_max"] = lambda_temp/n

    # hitung ci alternatif
    for data in alternatif:
        data[kriteria]["ci"] = (data[kriteria]["lambda_max"]-n)/(n-1)

    dataRC = [0, 0, 0.58, 1.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51, 1.48, 1.56, 1.57, 1.59]

    # hitung cr alternatif
    for data in alternatif:
        if n <= 15:
            data[kriteria]["cr"] = data[kriteria]["ci"]/dataRC[n-1]
        else:
            data[kriteria]["cr"] = data[kriteria]["ci"]/dataRC[14]

    return alternatif

def hitungKriteria(kriteria):

    n = 5

    # tambahkan kepentingan kriteria yang sama menjadi 1
    i = 0
    for data in kriteria:
        data[data["obj"]['pilihan'].lower()]["awal"][i] = 1
        i += 1

    # tambahkan kepentingan kriteria
    k = n-1
    batas_l = 0
    for i in range(n):
        l = batas_l + 1
        for j in range(k):
            kriteria[i][kriteria[i]["obj"]['pilihan'].lower()]["awal"][l] = 2
            kriteria[l][kriteria[l]["obj"]['pilihan'].lower()]["awal"][i] = 1/2
            l += 1
        batas_l += 1
        k -= 1

    jumlah = []
    # hitung jumlah tiap baris kriteria
    for data in kriteria:
        jumlah_temp = 0
        for i in range(n):
            jumlah_temp += data[data["obj"]['pilihan'].lower()]["awal"][i]
        jumlah.append(jumlah_temp)

    # hitung normalisasi matriks kriteria
    for data in kriteria:
        for i in range(n):
            data[data["obj"]['pilihan'].lower()]["normalisasi"][i] = data[data["obj"]['pilihan'].lower()]["awal"][i]/jumlah[i]

    # hitung weight kriteria
    for data in kriteria:
        weight_temp = 0
        for i in range(n):
            weight_temp += data[data["obj"]['pilihan'].lower()]["normalisasi"][i]
        data[data["obj"]['pilihan'].lower()]["weight"] = weight_temp/n

    # hitung matriks terbobot kriteria
    for data in kriteria:
        for i in range(n):
            data[data["obj"]['pilihan'].lower()]["terbobot"][i] = data[data["obj"]['pilihan'].lower()]["awal"][i]*data[data["obj"]['pilihan'].lower()]["weight"]

    # hitung wsv kriteria
    for data in kriteria:
        data[data["obj"]['pilihan'].lower()]["wsv"] = sum(data[data["obj"]['pilihan'].lower()]["terbobot"])

    # hitung cv kriteria
    for data in kriteria:
        data[data["obj"]['pilihan'].lower()]["cv"] = data[data["obj"]['pilihan'].lower()]["wsv"]/data[data["obj"]['pilihan'].lower()]["weight"]

    # hitung lambda_max kriteria
    lambda_temp = 0
    for data in kriteria:
        lambda_temp += data[data["obj"]['pilihan'].lower()]["cv"]
    for data in kriteria:
        data[data["obj"]['pilihan'].lower()]["lambda_max"] = lambda_temp/n

    # hitung ci kriteria
    for data in kriteria:
        data[data["obj"]['pilihan'].lower()]["ci"] = (data[data["obj"]['pilihan'].lower()]["lambda_max"]-n)/(n-1)

    dataRC = [0, 0, 0.58, 1.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51, 1.48, 1.56, 1.57, 1.59]

    # hitung cr kriteria
    for data in kriteria:
        if n <= 15:
            data[data["obj"]['pilihan'].lower()]["cr"] = data[data["obj"]['pilihan'].lower()]["ci"]/dataRC[n-1]
        else:
            data[data["obj"]['pilihan'].lower()]["cr"] = data[data["obj"]['pilihan'].lower()]["ci"]/dataRC[14]
        

    return kriteria