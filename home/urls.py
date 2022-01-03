from django.urls import path
# import from current directory
from . import views

urlpatterns = [
    path('', views.index, name='home')
]
