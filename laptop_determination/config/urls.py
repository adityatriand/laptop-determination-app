from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('laptop-selection/', include("laptop_selection.urls")),
    path('', views.index)
]
