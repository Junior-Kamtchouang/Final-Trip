from django.urls import path

from . import views 

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about', views.about, name='about'),
    path('finalTrip', views.finalTrip, name='finalTrip'),
    # Liste aller Associations
    path('associations/', views.association_list, name='association_list'),

    # Detailseite einer einzelnen Association
    path('associations/<int:pk>/', views.association_detail, name='association_detail'),
]
