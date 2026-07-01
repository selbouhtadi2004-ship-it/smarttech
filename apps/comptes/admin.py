from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import ProfilUtilisateur

class ProfilUtilisateurInline(admin.StackedInline):
    model = ProfilUtilisateur
    can_delete = False
    verbose_name_plural = 'Profil Utilisateur'

class UserAdmin(BaseUserAdmin):
    inlines = [ProfilUtilisateurInline]

# Remplacer le UserAdmin par défaut
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
