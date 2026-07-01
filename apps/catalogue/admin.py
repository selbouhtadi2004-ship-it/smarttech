from django.contrib import admin
from django.utils.html import format_html
from .models import Categorie, Produit, ImageProduit

class ImageProduitInline(admin.TabularInline):
    model = ImageProduit
    extra = 1

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'nombre_produits', 'est_active', 'date_creation')
    list_editable = ('est_active',)
    prepopulated_fields = {'slug': ('nom',)}

    def nombre_produits(self, obj):
        return obj.produits.count()
    nombre_produits.short_description = 'Nombre de produits'

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('apercu_image', 'nom', 'categorie', 'marque', 'prix', 'prix_promo', 'stock', 'est_disponible', 'est_en_vedette')
    list_editable = ('prix', 'prix_promo', 'stock', 'est_disponible', 'est_en_vedette')
    list_filter = ('categorie', 'est_disponible', 'est_en_vedette', 'marque')
    search_fields = ('nom', 'marque', 'reference', 'description')
    prepopulated_fields = {'slug': ('nom',)}
    inlines = [ImageProduitInline]

    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: contain;" />', obj.image.url)
        return "Pas d'image"
    apercu_image.short_description = 'Aperçu'
