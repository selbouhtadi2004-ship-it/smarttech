from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.panier.panier import Panier
from apps.catalogue.models import Produit
from .models import Commande, ArticleCommande
from .forms import CheckoutForm

@login_required
def checkout(request):
    panier = Panier(request)
    if panier.est_vide():
        messages.warning(request, "Votre panier est vide. Ajoutez des produits avant de passer commande.")
        return redirect('panier:panier_detail')
        
    profil = request.user.profil
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.utilisateur = request.user
            # Frais de livraison (offerts)
            commande.frais_livraison = 0.00
            
            commande.save()
            
            
            # Enregistrer les articles commandés et décrémenter le stock
            for item in panier:
                prod_id = item['produit']['id']
                db_prod = None
                
                # Essayer de trouver le produit dans la base de données réelle
                try:
                    db_prod = Produit.objects.get(id=prod_id)
                except Produit.DoesNotExist:
                    pass
                
                ArticleCommande.objects.create(
                    commande=commande,
                    produit=db_prod,
                    nom_produit=item['produit']['nom'],
                    prix_unitaire=item['prix'],
                    quantite=item['quantite']
                )
                
                # Décrémentation du stock si le produit existe en base
                if db_prod:
                    db_prod.stock -= item['quantite']
                    if db_prod.stock < 0:
                        db_prod.stock = 0
                    db_prod.save()
                    
            # Vider le panier
            panier.vider()
            messages.success(request, "Félicitations ! Votre commande a été enregistrée avec succès.")
            return redirect('commandes:confirmation', id=commande.id)
        else:
            messages.error(request, "Veuillez corriger les informations du formulaire.")
    else:
        # Pré-remplissage avec les informations du compte et du profil
        initial_data = {
            'nom_complet': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
            'telephone': profil.telephone,
            'adresse_livraison': profil.adresse,
            'ville': profil.ville,
            'code_postal': profil.code_postal,
        }
        form = CheckoutForm(initial=initial_data)
        
    return render(request, 'commandes/checkout.html', {'form': form, 'panier': panier})

@login_required
def confirmation(request, id):
    # Vérifie que la commande existe et appartient bien à l'utilisateur connecté
    commande = get_object_or_404(Commande, id=id, utilisateur=request.user)
    return render(request, 'commandes/confirmation.html', {'commande': commande})

@login_required
def historique(request):
    commandes = request.user.commandes.all().order_by('-date_commande')
    return render(request, 'commandes/historique.html', {'commandes': commandes})

@login_required
def detail_commande(request, id):
    # Vérifie que la commande existe et appartient bien à l'utilisateur connecté
    commande = get_object_or_404(Commande, id=id, utilisateur=request.user)
    return render(request, 'commandes/detail_commande.html', {'commande': commande})
