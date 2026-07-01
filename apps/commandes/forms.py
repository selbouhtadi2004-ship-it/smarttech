from django import forms
from apps.comptes.forms import valider_telephone_marocain
from .models import Commande, MODE_PAIEMENT_CHOICES


class CheckoutForm(forms.ModelForm):
    nom_complet = forms.CharField(
        label="Nom Complet",
        widget=forms.TextInput(attrs={'placeholder': 'Prénom et Nom'})
    )

    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'placeholder': 'exemple@email.com'})
    )

    telephone = forms.CharField(
        label="Téléphone de contact",
        validators=[valider_telephone_marocain],
        widget=forms.TextInput(attrs={'placeholder': '06 00 00 00 00'})
    )

    adresse_livraison = forms.CharField(
        label="Adresse de livraison complète",
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': "Rue, Quartier, Numéro d'appartement..."})
    )

    ville = forms.CharField(
        label="Ville",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Casablanca'})
    )

    code_postal = forms.CharField(
        label="Code Postal",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: 20000'})
    )

    mode_paiement = forms.ChoiceField(
        label="Mode de paiement",
        choices=MODE_PAIEMENT_CHOICES,
        widget=forms.RadioSelect
    )

    notes = forms.CharField(
        label="Instructions / Notes de livraison (optionnel)",
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Indications particulières pour le livreur...'})
    )

    class Meta:
        model = Commande
        fields = [
            'nom_complet',
            'email',
            'telephone',
            'adresse_livraison',
            'ville',
            'code_postal',
            'mode_paiement',
            'notes',
        ]