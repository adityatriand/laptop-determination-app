from django.urls import path
from . import views

urlpatterns = [
    path('alternatives/', views.alternatives),
    path('search/', views.search),
    path('results/', views.results)
]