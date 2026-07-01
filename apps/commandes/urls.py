from django.urls import path
from . import views

app_name = 'commandes'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<int:id>/', views.confirmation, name='confirmation'),
    path('historique/', views.historique, name='historique'),
    path('detail/<int:id>/', views.detail_commande, name='detail_commande'),
]
