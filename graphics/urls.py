from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_graphics, name='graphics'),
    path('<int:graphic_id>/', views.graphic_detail, name='graphic_detail'),
    path('add/', views.add_graphic, name='add_graphic'),
    path('edit/<int:graphic_id>/', views.edit_graphic, name='edit_graphic'),
    path('delete/<int:graphic_id>/', views.delete_graphic, name='delete_graphic'),
]
