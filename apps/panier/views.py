from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from apps.catalogue.views import get_processed_products
from .panier import Panier

def panier_detail(request):
    panier = Panier(request)
    return render(request, 'panier/panier.html', {'panier': panier})

@require_POST
def ajouter_au_panier(request, id):
    panier = Panier(request)
    
    # Vérifie si le produit existe
    produits = get_processed_products()
    produit = next((p for p in produits if p['id'] == id), None)
    if not produit:
        messages.error(request, "Produit introuvable.")
        return redirect('catalogue:accueil')
        
    quantite = int(request.POST.get('quantite', 1))
    
    # Vérifier le stock
    if produit['stock'] <= 0 or not produit['est_disponible']:
        messages.error(request, f"Le produit {produit['nom']} est en rupture de stock.")
        return redirect(request.META.get('HTTP_REFERER', 'catalogue:accueil'))
        
    # Ajouter
    success = panier.ajouter(produit_id=id, quantite=quantite)
    if success:
        messages.success(request, f"Le produit {produit['nom']} a été ajouté à votre panier.")
    else:
        messages.error(request, "Une erreur est survenue lors de l'ajout au panier.")
        
    return redirect('panier:panier_detail')

@require_POST
def modifier_panier(request, id):
    panier = Panier(request)
    
    # Vérifie si le produit existe
    produits = get_processed_products()
    produit = next((p for p in produits if p['id'] == id), None)
    if not produit:
        messages.error(request, "Produit introuvable.")
        return redirect('panier:panier_detail')
        
    quantite = int(request.POST.get('quantite', 1))
    
    # Vérifier le stock disponible
    if quantite > produit['stock']:
        quantite = produit['stock']
        messages.warning(request, f"La quantité demandée a été limitée au stock disponible ({produit['stock']} unités).")

    # Mettre à jour (override_quantite=True)
    panier.ajouter(produit_id=id, quantite=quantite, override_quantite=True)
    messages.success(request, f"Quantité mise à jour pour {produit['nom']}.")
    return redirect('panier:panier_detail')

def supprimer_du_panier(request, id):
    panier = Panier(request)
    
    produits = get_processed_products()
    produit = next((p for p in produits if p['id'] == id), None)
    
    panier.supprimer(produit_id=id)
    if produit:
        messages.info(request, f"Le produit {produit['nom']} a été retiré de votre panier.")
    else:
        messages.info(request, "Produit retiré du panier.")
        
    return redirect('panier:panier_detail')
