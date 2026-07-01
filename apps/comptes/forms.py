import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import ProfilUtilisateur

def valider_telephone_marocain(value):
    # Regex pour les numéros marocains : commence par 06, 07, 05 ou +212 / 212
    pattern = re.compile(r'^(05|06|07|\+212|212)[0-9]{8}$')
    if not pattern.match(value.replace(" ", "").replace("-", "")):
        raise ValidationError("Le numéro de téléphone doit être un numéro marocain valide (commençant par 05, 06, 07 ou +212).")

class InscriptionForm(forms.Form):
    first_name = forms.CharField(label="Prénom", max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Votre prénom'}))
    last_name = forms.CharField(label="Nom", max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Votre nom'}))
    email = forms.EmailField(label="Adresse Email", widget=forms.EmailInput(attrs={'placeholder': 'exemple@email.com'}))
    telephone = forms.CharField(label="Téléphone", validators=[valider_telephone_marocain], widget=forms.TextInput(attrs={'placeholder': '06 00 00 00 00'}))
    adresse = forms.CharField(label="Adresse de livraison", widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Adresse complète...'}))
    ville = forms.CharField(label="Ville", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Ex: Casablanca'}))
    code_postal = forms.CharField(label="Code Postal", max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Ex: 20000'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'placeholder': 'Minimum 6 caractères'}))
    password_confirm = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput(attrs={'placeholder': 'Répétez le mot de passe'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà enregistrée.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Les mots de passe ne correspondent pas.")
        return cleaned_data

class ConnexionForm(forms.Form):
    email = forms.EmailField(label="Adresse Email", widget=forms.EmailInput(attrs={'placeholder': 'exemple@email.com'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'placeholder': 'Votre mot de passe'}))

class ProfilForm(forms.ModelForm):
    first_name = forms.CharField(label="Prénom", max_length=150)
    last_name = forms.CharField(label="Nom", max_length=150)
    email = forms.EmailField(label="Adresse Email")
    telephone = forms.CharField(label="Téléphone", validators=[valider_telephone_marocain], required=False)
    adresse = forms.CharField(label="Adresse", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    ville = forms.CharField(label="Ville", max_length=100, required=False)
    code_postal = forms.CharField(label="Code Postal", max_length=10, required=False)
    avatar = forms.ImageField(label="Photo de profil", required=False, widget=forms.FileInput(attrs={'id': 'avatar-input', 'accept': 'image/*'}))

    class Meta:
        model = ProfilUtilisateur
        fields = ['telephone', 'adresse', 'ville', 'code_postal', 'avatar']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.user.id).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée par un autre utilisateur.")
        return email

    def save(self, commit=True):
        profil = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            self.user.username = self.cleaned_data['email'].split('@')[0]
            if commit:
                self.user.save()
                profil.save()
        return profil
