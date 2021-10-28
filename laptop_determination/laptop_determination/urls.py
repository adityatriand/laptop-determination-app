from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mylaptop/', include("mylaptop.urls")),
    path('', views.index)
]
