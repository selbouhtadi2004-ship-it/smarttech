from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    # Accueil
    path('', views.accueil, name='accueil'),

    # Produits
    path('produits/', views.liste_produits, name='liste_produits'),
    path('categorie/<slug:slug>/', views.liste_categorie, name='liste_categorie'),
    path('produit/<int:id>/<slug:slug>/', views.detail_produit, name='detail_produit'),
    path('recherche/', views.recherche, name='recherche'),

    # Pages
    path('devis/', views.devis, name='devis'),
    path('contact/', views.contact_view, name='contact'),

    # Footer
    path('qui-sommes-nous/', views.qui_sommes_nous, name='qui_sommes_nous'),
    path('nos-magasins/', views.nos_magasins, name='nos_magasins'),
    path('conditions-generales/', views.conditions_generales, name='conditions_generales'),
    path('politique-retour/', views.politique_retour, name='politique_retour'),
    path('garantie-sav/', views.garantie, name='garantie'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
    path(
    "favoris/",
    views.mes_favoris,
    name="mes_favoris"
),

path(
    "favori/<int:produit_id>/",
    views.ajouter_favori,
    name="ajouter_favori"
),
]