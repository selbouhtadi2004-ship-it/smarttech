from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    icon = models.CharField(max_length=50, default="bi-grid")
    description = models.TextField(blank=True, null=True)
    est_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    nom = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    marque = models.CharField(max_length=100)
    reference = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    description_courte = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_promo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(default=0)
    est_disponible = models.BooleanField(default=True)
    est_en_vedette = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nom)
            slug = base_slug
            i = 1

            while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{i}"
                i += 1

            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def prix_effectif(self):
        if self.prix_promo:
            return self.prix_promo
        return self.prix

    @property
    def est_en_promo(self):
        return self.prix_promo is not None

    @property
    def pourcentage_reduction(self):
        if self.prix_promo and self.prix > 0:
            reduction = ((self.prix - self.prix_promo) / self.prix) * 100
            return round(reduction)
        return 0

    def __str__(self):
        return f"{self.nom} ({self.marque})"

class ImageProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='produits/galerie/')
    alt = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Image pour {self.produit.nom}"


class HeroSlide(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.TextField()
    image = models.ImageField(upload_to="hero/")
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Favori(models.Model):
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favoris"
    )

    produit = models.ForeignKey(
        "Produit",
        on_delete=models.CASCADE,
        related_name="favoris"
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("utilisateur", "produit")

    def __str__(self):
        return f"{self.utilisateur.username} - {self.produit.nom}"


class Marque(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='marques/')
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.nom