from decimal import Decimal
from django.conf import settings
from apps.catalogue.views import get_processed_products

class Panier:
    def __init__(self, request):
        """
        Initialise le panier.
        """
        self.session = request.session
        panier = self.session.get(settings.CART_SESSION_ID)
        if not panier:
            # Enregistrer un panier vide dans la session
            panier = self.session[settings.CART_SESSION_ID] = {}
        self.panier = panier

    def ajouter(self, produit_id, quantite=1, override_quantite=False):
        """
        Ajoute un produit au panier ou met à jour sa quantité.
        """
        produit_id = str(produit_id)
        # Récupère les infos du produit de démo
        produits = get_processed_products()
        produit = next((p for p in produits if str(p['id']) == produit_id), None)
        
        if not produit:
            return False

        if produit_id not in self.panier:
            # Stocke le prix effectif (avec promo si applicable)
            self.panier[produit_id] = {
                'quantite': 0,
                'prix': str(produit['prix_effectif'])
            }

        if override_quantite:
            self.panier[produit_id]['quantite'] = quantite
        else:
            self.panier[produit_id]['quantite'] += quantite

        # Limite la quantité par rapport au stock du produit de démo
        if self.panier[produit_id]['quantite'] > produit['stock']:
            self.panier[produit_id]['quantite'] = produit['stock']
            
        self.sauvegarder()
        return True

    def supprimer(self, produit_id):
        """
        Supprime un produit du panier.
        """
        produit_id = str(produit_id)
        if produit_id in self.panier:
            del self.panier[produit_id]
            self.sauvegarder()

    def sauvegarder(self):
        # Indique à Django que la session a été modifiée
        self.session.modified = True

    def vider(self):
        # Supprime le panier de la session
        del self.session[settings.CART_SESSION_ID]
        self.sauvegarder()

    def get_total(self):
        """
        Calcule le prix total du panier.
        """
        return sum(Decimal(item['prix']) * item['quantite'] for item in self.panier.values())

    def est_vide(self):
        return len(self.panier) == 0

    def __iter__(self):
        """
        Boucle sur les articles du panier et récupère les produits associés.
        """
        produit_ids = self.panier.keys()
        produits = get_processed_products()
        
        # Filtrer et enrichir les items
        for p_id in produit_ids:
            produit = next((p for p in produits if str(p['id']) == p_id), None)
            if produit:
                item = self.panier[p_id].copy()
                item['produit'] = produit
                item['prix'] = Decimal(item['prix'])
                item['prix_total'] = item['prix'] * item['quantite']
                yield item

    def __len__(self):
        """
        Compte le nombre total d'articles dans le panier.
        """
        return sum(item['quantite'] for item in self.panier.values())
