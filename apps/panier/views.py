from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from apps.catalogue.views import get_processed_products
from .panier import Panier
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.catalogue.models import Produit
from .models import Wishlist

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
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': "Produit introuvable."})
        messages.error(request, "Produit introuvable.")
        return redirect(request.META.get('HTTP_REFERER', 'catalogue:accueil'))
        
    quantite = int(request.POST.get('quantite', 1))
    
    # Vérifier le stock
    if produit['stock'] <= 0 or not produit['est_disponible']:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': f"Le produit {produit['nom']} est en rupture de stock."})
        messages.error(request, f"Le produit {produit['nom']} est en rupture de stock.")
        return redirect(request.META.get('HTTP_REFERER', 'catalogue:accueil'))
        
    # Ajouter
    success = panier.ajouter(produit_id=id, quantite=quantite)
    if success:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Le produit '{produit['nom']}' a été ajouté à votre panier.",
                'total_items': len(panier),
                'total_price': float(panier.get_total())
            })
        messages.success(request, f"Le produit {produit['nom']} a été ajouté à votre panier.")
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': "Une erreur est survenue lors de l'ajout au panier."})
        messages.error(request, "Une erreur est survenue lors de l'ajout au panier.")
        
    return redirect(request.META.get('HTTP_REFERER', 'catalogue:accueil'))

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
    
def toggle_wishlist(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    fav, created = Wishlist.objects.get_or_create(
        user=request.user,
        produit=produit
    )

    if created:
        return JsonResponse({"status": "added"})

    fav.delete()
    return JsonResponse({"status": "removed"})
@login_required
def wishlist(request):
    favoris = Wishlist.objects.filter(user=request.user).select_related("produit")

    return render(request, "panier/wishlist.html", {
        "favoris": favoris
    })