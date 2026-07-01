from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('produits/', views.liste_produits, name='liste_produits'),
    path('categorie/<slug:slug>/', views.liste_categorie, name='liste_categorie'),
    path('produit/<int:id>/<slug:slug>/', views.detail_produit, name='detail_produit'),
    path('recherche/', views.recherche, name='recherche'),
    path('devis/', views.devis, name='devis'),   
    path('contact/', views.contact_view, name='contact'),
]