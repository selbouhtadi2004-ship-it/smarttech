from .panier import Panier

def panier_context(request):
    """
    Rend l'objet panier disponible dans tous les templates Django.
    """
    return {'panier': Panier(request)}
