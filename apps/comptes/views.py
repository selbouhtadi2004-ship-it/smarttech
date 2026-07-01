from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm, ProfilForm

# Mock de 3 commandes précédentes pour le profil utilisateur (pour le rendu frontend)
MOCK_COMMANDES = [
    {
        'id': 1045,
        'date_commande': '2026-06-15',
        'total_commande': 14200.00,
        'nombre_articles': 2,
        'statut': 'livree',
        'statut_label': 'Livrée',
        'frais_livraison': 0.00,
    },
    {
        'id': 1021,
        'date_commande': '2026-05-10',
        'total_commande': 999.00,
        'nombre_articles': 1,
        'statut': 'confirmee',
        'statut_label': 'Confirmée',
        'frais_livraison': 0.00,
    },
    {
        'id': 998,
        'date_commande': '2026-04-02',
        'total_commande': 700.00,
        'nombre_articles': 1,
        'statut': 'annulee',
        'statut_label': 'Annulée',
        'frais_livraison': 0.00,
    }
]

def inscription(request):
    if request.user.is_authenticated:
        return redirect('catalogue:accueil')
        
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Création du user
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            # Assurer l'unicité du username
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
                
            user = User.objects.create_user(
                username=username,
                email=email,
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # Le signal post_save a créé le ProfilUtilisateur, nous mettons à jour ses champs
            profil = user.profil
            profil.telephone = form.cleaned_data['telephone']
            profil.adresse = form.cleaned_data['adresse']
            profil.ville = form.cleaned_data['ville']
            profil.code_postal = form.cleaned_data['code_postal']
            profil.save()
            
            # Connexion automatique
            login(request, user)
            messages.success(request, f"Inscription réussie ! Bienvenue {user.first_name}.")
            return redirect('catalogue:accueil')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = InscriptionForm()
        
    return render(request, 'comptes/inscription.html', {'form': form})

def connexion(request):
    if request.user.is_authenticated:
        return redirect('catalogue:accueil')
        
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Recherche de l'utilisateur par email
            user_obj = User.objects.filter(email=email).first()
            if user_obj:
                # Authentification par le username associé
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Ravi de vous revoir, {user.first_name} !")
                    next_url = request.GET.get('next', 'catalogue:accueil')
                    if next_url != 'catalogue:accueil' and not next_url.startswith('/'):
                        next_url = 'catalogue:accueil'
                    return redirect(next_url)
            
            messages.error(request, "Adresse email ou mot de passe incorrect.")
    else:
        form = ConnexionForm()
        
    return render(request, 'comptes/connexion.html', {'form': form})

def deconnexion(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('catalogue:accueil')

@login_required
def profil(request):
    profil_obj = request.user.profil
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=profil_obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect('comptes:profil')
        else:
            messages.error(request, "Veuillez corriger les erreurs de saisie.")
    else:
        form = ProfilForm(instance=profil_obj, user=request.user)
        
    context = {
        'form': form,
        'commandes': MOCK_COMMANDES, # Pour l'affichage de l'historique sur le profil
    }
    return render(request, 'comptes/profil.html', context)
