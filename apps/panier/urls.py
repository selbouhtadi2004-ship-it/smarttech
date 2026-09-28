from django.urls import path
from . import views

app_name = 'panier'

urlpatterns = [
    path('', views.panier_detail, name='panier_detail'),
    path('ajouter/<int:id>/', views.ajouter_au_panier, name='ajouter'),
    path('modifier/<int:id>/', views.modifier_panier, name='modifier'),
    path('supprimer/<int:id>/', views.supprimer_du_panier, name='supprimer'),
 path(
    "wishlist/toggle/<int:produit_id>/",
    views.toggle_wishlist,
    name="toggle_wishlist",),
    path(
    "wishlist/",
    views.wishlist,
    name="wishlist",
),
]

