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
    return render(request, 'mylaptop/cari.html')

def hasil(request):
    return render(request, 'mylaptop/hasil.html')