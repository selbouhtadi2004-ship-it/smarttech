# 🚀 PROMPT ANTIGRAVITY — Projet InnovaTech E-Commerce

> Copie-colle ce prompt tel quel dans Antigravity pour générer le projet complet.

---

## PROMPT PRINCIPAL (à coller dans Antigravity)

```
Tu es un expert en développement web full-stack. Crée un site e-commerce complet 
appelé "InnovaTech" pour une entreprise marocaine qui vend du matériel informatique. 
Voici les spécifications exactes :

─────────────────────────────────────────
STACK TECHNIQUE
─────────────────────────────────────────
- Backend  : Django 4.2 (Python)
- Frontend : HTML5 + CSS3 + Bootstrap 5 + JavaScript vanilla
- Base de données : SQLite
- Librairies Django : Pillow, django-crispy-forms, crispy-bootstrap5, python-decouple

─────────────────────────────────────────
STRUCTURE DU PROJET
─────────────────────────────────────────
Crée un projet Django nommé "innovatech" avec 4 applications :
1. apps/catalogue   → produits & catégories
2. apps/comptes     → authentification & profils
3. apps/panier      → panier en session Django
4. apps/commandes   → commandes & checkout

─────────────────────────────────────────
MODÈLES DE BASE DE DONNÉES
─────────────────────────────────────────

### App catalogue :
- Categorie : nom, slug (auto-généré), image, description, est_active, date_creation
- Produit : categorie (FK), nom, slug, marque, reference (unique), description, 
  description_courte, image, prix (DecimalField), prix_promo (nullable), 
  stock, est_disponible, est_en_vedette, date_creation, date_modification
  → Propriétés : prix_effectif, est_en_promo, pourcentage_reduction
- ImageProduit : produit (FK), image, alt

### App comptes :
- ProfilUtilisateur (OneToOne avec User Django) : telephone, adresse, ville, 
  code_postal, date_naissance, avatar
  → Signal post_save pour créer le profil automatiquement

### App commandes :
- Commande : utilisateur (FK User), nom_complet, email, telephone, 
  adresse_livraison, ville, code_postal, statut (choices: en_attente/confirmee/
  en_preparation/expediee/livree/annulee), date_commande, frais_livraison, notes
  → Propriétés : total_produits, total_commande, nombre_articles
- ArticleCommande : commande (FK), produit (FK), nom_produit, prix_unitaire, 
  quantite → méthode get_total()

─────────────────────────────────────────
FONCTIONNALITÉS À DÉVELOPPER
─────────────────────────────────────────

### 1. CATALOGUE
- Page d'accueil : bannière hero, bande avantages, grille catégories, 
  produits en vedette (8 max), nouveautés (8 max)
- Liste produits : tous les produits avec tri (récent/prix asc/prix desc/nom)
- Liste par catégorie : filtre par slug de catégorie
- Détail produit : images, prix avec promo, stock, bouton ajout panier, 
  produits similaires (4 max, même catégorie)
- Recherche : filtre sur nom + description + marque + reference (Q objects Django)

### 2. AUTHENTIFICATION
- Inscription : prénom, nom, email (unique), mot de passe + confirmation
  → username auto-généré depuis l'email (partie avant @)
  → Connexion automatique après inscription
- Connexion par email (pas par username)
- Déconnexion
- Profil utilisateur : modifier infos + voir 5 dernières commandes
- Validation téléphone marocain (commence par 06/07/05/+212)

### 3. PANIER (stocké en session Django)
- Classe Panier dans apps/panier/panier.py
  → Méthodes : ajouter(), supprimer(), sauvegarder(), vider(), get_total(), est_vide()
  → __iter__ retourne les articles avec produit Django, prix Decimal, prix_total
  → __len__ retourne la somme des quantités
- Context processor : panier disponible dans TOUS les templates via {{ panier }}
- Vues : detail_panier, ajouter_au_panier (POST only), modifier_panier (POST only), 
  supprimer_du_panier
- Vérification du stock avant ajout
- Modification de quantité directement dans le tableau du panier (onchange submit)

### 4. COMMANDES
- Checkout (login_required) : 
  → Redirect si panier vide
  → Pré-remplissage avec les infos du profil utilisateur
  → Création Commande + ArticleCommande en base
  → Décrémentation du stock des produits commandés
  → Vidage du panier après confirmation
- Page de confirmation avec récapitulatif
- Historique des commandes (login_required)
- Détail d'une commande (login_required, vérifier que c'est bien sa commande)
- Mode de paiement : CASH À LA LIVRAISON UNIQUEMENT (pas de paiement en ligne)

─────────────────────────────────────────
INTERFACE UTILISATEUR
─────────────────────────────────────────

### Design général :
- Inspiré de iris.ma (leader vente matériel informatique Maroc)
- Couleur principale : bleu Bootstrap (#0d6efd)
- Accents : jaune/warning (#ffc107)
- Police : Segoe UI / system-ui
- Entièrement en FRANÇAIS

### Navbar (sticky, dark, bg-primary) :
- Logo "InnovaTech" avec icône bi-cpu-fill à gauche
- Barre de recherche centrale (40% de largeur)
- Menu droite : dropdown Catégories, icône Panier avec badge rouge (nb articles), 
  dropdown utilisateur (Profil / Mes commandes / Admin si staff / Déconnexion)
  ou boutons Connexion + S'inscrire si non connecté

### Carte produit (réutilisable _carte_produit.html) :
- Badge promo rouge "-XX%" en position absolute top-right si en promo
- Image avec hover zoom léger
- Marque en petit + nom tronqué à 60 chars
- Prix barré + prix promo en rouge OU prix normal en bleu
- Bouton "Ajouter au panier" (POST form) ou "Rupture de stock" désactivé
- Hover : translateY(-5px) + box-shadow

### Page panier :
- Tableau avec image + nom + prix unitaire + input quantité (auto-submit onchange) 
  + prix total ligne + bouton supprimer
- Carte récapitulatif sticky : sous-total, badge "Cash à la livraison", total, 
  bouton "Valider la commande" (ou "Se connecter pour commander" si non auth)

### Page checkout :
- Formulaire en 2 colonnes : infos livraison (gauche) + récapitulatif panier (droite)
- Champs : nom complet, email, téléphone, adresse, ville, code postal, notes
- Section paiement : badge vert "Cash à la livraison" avec explication

### Footer :
- 4 colonnes : présentation InnovaTech, liens catalogue, liens compte, contact+badges
- Badges : "Livraison COD" vert + "Achat sécurisé" bleu
- Copyright EMSI PFA

─────────────────────────────────────────
ADMINISTRATION DJANGO
─────────────────────────────────────────
- CategorieAdmin : list_display avec nombre de produits, list_editable est_active, 
  prepopulated_fields pour slug
- ProduitAdmin : list_display avec aperçu image (format_html), list_editable prix/stock/
  disponibilité/vedette, TabularInline pour ImageProduit, search + filters
- CommandeAdmin : list_display avec total, list_editable statut, 
  TabularInline readonly pour ArticleCommande, filtres par statut/ville/date

─────────────────────────────────────────
CONFIGURATION SETTINGS.PY
─────────────────────────────────────────
- LANGUAGE_CODE = 'fr-fr'
- TIME_ZONE = 'Africa/Casablanca'
- MEDIA_URL/ROOT configurés pour les images uploadées
- STATICFILES_DIRS = [BASE_DIR / 'static']
- LOGIN_URL = '/comptes/connexion/'
- LOGIN_REDIRECT_URL = '/'
- CART_SESSION_ID = 'panier'
- CRISPY_TEMPLATE_PACK = 'bootstrap5'
- Context processor panier : 'apps.panier.context_processors.panier_context'
- Templates dans BASE_DIR / 'templates'

─────────────────────────────────────────
FICHIERS STATIQUES
─────────────────────────────────────────
CSS (static/css/style.css) :
- Variables CSS : --primary, --warning, --transition
- Hero gradient : linear-gradient(135deg, #0d6efd, #0a3d91)
- .product-card : hover translateY(-5px) + box-shadow + zoom image
- .category-card : hover background bleu + texte blanc
- Classes statut commande : .statut-en_attente, .statut-confirmee, etc.
- Responsive mobile : pas de hover transform sur mobile

JS (static/js/main.js) :
- Auto-fermeture des alertes succès/info après 4 secondes
- Boutons +/- pour la quantité sur la page détail produit
- Aperçu image avatar sur la page profil (FileReader API)

─────────────────────────────────────────
URLS COMPLÈTES À CRÉER
─────────────────────────────────────────
/                                → accueil
/produits/                       → liste tous produits
/categorie/<slug>/               → liste par catégorie
/produit/<id>/<slug>/            → détail produit
/recherche/?q=                   → recherche
/comptes/inscription/            → inscription
/comptes/connexion/              → connexion
/comptes/deconnexion/            → déconnexion
/comptes/profil/                 → profil (login_required)
/panier/                         → voir panier
/panier/ajouter/<id>/            → ajouter (POST)
/panier/modifier/<id>/           → modifier quantité (POST)
/panier/supprimer/<id>/          → supprimer article
/commandes/checkout/             → passer commande (login_required)
/commandes/confirmation/<id>/    → confirmation (login_required)
/commandes/historique/           → mes commandes (login_required)
/commandes/detail/<id>/          → détail commande (login_required)
/admin/                          → interface admin Django

─────────────────────────────────────────
FICHIERS À CRÉER (liste complète)
─────────────────────────────────────────
innovatech/settings.py
innovatech/urls.py
apps/catalogue/models.py
apps/catalogue/views.py
apps/catalogue/urls.py
apps/catalogue/admin.py
apps/comptes/models.py
apps/comptes/views.py
apps/comptes/urls.py
apps/comptes/forms.py
apps/panier/panier.py
apps/panier/views.py
apps/panier/urls.py
apps/panier/context_processors.py
apps/commandes/models.py
apps/commandes/views.py
apps/commandes/urls.py
apps/commandes/forms.py
apps/commandes/admin.py
templates/base.html
templates/catalogue/accueil.html
templates/catalogue/liste_produits.html
templates/catalogue/detail_produit.html
templates/catalogue/_carte_produit.html
templates/catalogue/recherche.html
templates/comptes/inscription.html
templates/comptes/connexion.html
templates/comptes/profil.html
templates/panier/panier.html
templates/commandes/checkout.html
templates/commandes/confirmation.html
templates/commandes/historique.html
templates/commandes/detail_commande.html
static/css/style.css
static/js/main.js
requirements.txt
.env
.gitignore

─────────────────────────────────────────
COMMANDES DE DÉMARRAGE
─────────────────────────────────────────
Après génération du code, exécute dans l'ordre :
1. pip install -r requirements.txt
2. python manage.py makemigrations
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py runserver

Le site doit être accessible sur http://127.0.0.1:8000
L'admin sur http://127.0.0.1:8000/admin
```

---

## PROMPT DE SUIVI (si Antigravity demande des précisions)

Si l'IDE te demande des détails supplémentaires, réponds avec ces prompts :

### Pour le frontend uniquement :
```
Génère tous les templates HTML manquants avec Bootstrap 5. 
Chaque page doit étendre base.html avec {% extends 'base.html' %}.
Utilise les icônes Bootstrap Icons (bi-*).
Tout le texte doit être en français.
Le panier doit afficher {{ panier|length }} dans le badge de la navbar.
```

### Pour corriger un bug :
```
Le projet est un e-commerce Django nommé InnovaTech.
[Décris le bug ici]
Corrige en respectant la structure existante des apps : 
catalogue, comptes, panier, commandes.
```

### Pour ajouter des données de démo :
```
Crée un fichier fixtures/demo.json avec :
- 4 catégories : Laptops, Périphériques, Composants, Téléphones
- 12 produits répartis dans ces catégories avec des prix en MAD
- Commande la création avec : python manage.py loaddata fixtures/demo.json
```

---

## NOTES IMPORTANTES

- **Paiement** : Cash à la livraison UNIQUEMENT, pas de Stripe/PayPal
- **Langue** : Tout en français (interface, messages d'erreur, labels)
- **Base de données** : SQLite (fichier db.sqlite3 local)
- **Images** : Stockées dans le dossier `media/` via Pillow
- **Sécurité** : Toujours utiliser {% csrf_token %} dans les formulaires POST
- **Auth** : Connexion par email (pas par username), login_required sur les pages sensibles
