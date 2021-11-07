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
    data = models.Laptops.objects.all().order_by('company')
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

        context = {
            'cari': data
        }

        return render(request, 'mylaptop/hasil.html', context)

    else:
        return HttpResponseRedirect('/mylaptop/cari/')
        # return render(request, 'mylaptop/hasil.html')