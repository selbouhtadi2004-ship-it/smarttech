from django.db import models
from django.contrib.auth.models import User
from apps.catalogue.models import Produit


MODE_PAIEMENT_CHOICES = [
    ('carte', 'Carte bancaire'),
    ('cod', 'Paiement à la livraison (COD)'),
    ('virement', 'Virement bancaire'),
]


class Commande(models.Model):

    STATUT_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('confirmee', 'Confirmée'),
        ('en_preparation', 'En cours de préparation'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')

    nom_complet = models.CharField(max_length=150)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)

    adresse_livraison = models.TextField()
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)

    mode_paiement = models.CharField(
        max_length=20,
        choices=MODE_PAIEMENT_CHOICES,
        default='cod'
    )

    statut = models.CharField(max_length=30, choices=STATUT_CHOICES, default='en_attente')

    date_commande = models.DateTimeField(auto_now_add=True)

    frais_livraison = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Commande #{self.id} de {self.nom_complet}"

    @property
    def total_produits(self):
        return sum(article.total_ligne for article in self.articles.all())

    @property
    def total_commande(self):
        return self.total_produits + self.frais_livraison

    @property
    def nombre_articles(self):
        return sum(article.quantite for article in self.articles.all())


class ArticleCommande(models.Model):

    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='articles')

    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, blank=True)

    nom_produit = models.CharField(max_length=200)

    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.nom_produit} (Commande #{self.commande.id})"

    @property
    def total_ligne(self):
        return self.prix_unitaire * self.quantite