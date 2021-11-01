from django.core import serializers
from django.shortcuts import render
from . import models

# Create your views here.
def alternatif(request):
    data = models.Laptops.objects.all()
    context = {
        'laptops': data,
    }
    return render(request, 'mylaptop/alternatif.html', context)

def cari(request):
    data = models.Laptops.objects.all().order_by('company')
    criterions = ['Pilih Kepentingan','Harga','RAM','CPU','SSD','HDD']
    unique_brands = []
    brands = []
    for x in data:
        # check if exists in unique_brands or not
        if x.company not in brands:
            unique_brands.append(x)
            brands.append(x.company)

    context = {
        'brands': unique_brands,
        'criterias':criterions
    }

    return render(request, 'mylaptop/cari.html', context)

def hasil(request):
    return render(request, 'mylaptop/hasil.html')