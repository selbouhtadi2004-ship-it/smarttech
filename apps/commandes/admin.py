from django.contrib import admin
from .models import Commande, ArticleCommande


class ArticleCommandeInline(admin.TabularInline):
    model = ArticleCommande
    extra = 0

    readonly_fields = (
        'produit',
        'nom_produit',
        'prix_unitaire',
        'quantite',
        'total_ligne_display',
    )

    can_delete = False

    def total_ligne_display(self, obj):
        if obj and obj.pk:
            return f"{obj.total_ligne} MAD"
        return "-"

    total_ligne_display.short_description = "Montant Ligne"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nom_complet',
        'ville',
        'telephone',
        'statut',
        'date_commande',
        'montant_total',
    )

    list_editable = ('statut',)

    list_filter = ('statut', 'ville', 'date_commande')

    search_fields = (
        'nom_complet',
        'email',
        'telephone',
        'id',
    )

    inlines = [ArticleCommandeInline]

    def montant_total(self, obj):
        return f"{obj.total_commande or 0} MAD"

    montant_total.short_description = "Montant de la commande"