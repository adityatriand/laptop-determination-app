from django.urls import path
from . import views

urlpatterns = [
    path('alternatif/', views.alternatif),
    path('cari/', views.cari),
    path('hasil/', views.hasil)
]