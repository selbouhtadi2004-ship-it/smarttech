from django.db import models
from django.contrib.auth.models import User
from apps.catalogue.models import Produit

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'produit')