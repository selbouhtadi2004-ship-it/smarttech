from .models import Categorie, Produit

def global_data(request):
    return {
        'categories': Categorie.objects.filter(est_active=True),
        'marques': Produit.objects.values_list('marque', flat=True).distinct(),
    }