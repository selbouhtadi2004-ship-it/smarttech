from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class ProfilUtilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=10, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

# Signal pour créer le profil utilisateur automatiquement lors de la création d'un utilisateur Django
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfilUtilisateur.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Sécurité si le profil n'existe pas encore
    if not hasattr(instance, 'profil'):
        ProfilUtilisateur.objects.create(user=instance)
    instance.profil.save()
