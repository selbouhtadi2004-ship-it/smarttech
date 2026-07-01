from django.shortcuts import render, Http404, get_object_or_404
from apps.catalogue.models import Produit, Categorie

# Catégories de Démo
Categorie.objects.filter(est_active=True)

# Produits de Démo (Mocks)
PRODUITS = [
    {
        'id': 1,
        'nom': 'ASUS ROG Strix G16 (2024)',
        'slug': 'asus-rog-strix-g16-2024',
        'marque': 'ASUS',
        'reference': 'ROG-G16-987',
        'description': 'Le PC portable de jeu ROG Strix G16 de 16 pouces offre des performances de pointe avec le processeur Intel Core i7 de 13e génération et la carte graphique NVIDIA GeForce RTX 4060. Écran FHD+ 165Hz, 16 Go de RAM DDR5 et 512 Go SSD NVMe. Système de refroidissement ROG Intelligent Cooling pour des sessions intenses.',
        'description_courte': 'Intel i7-13650HX, RTX 4060, 16Go RAM, 512Go SSD, 165Hz.',
        'image': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&auto=format&fit=crop&q=60',
        'prix': 15000.00,
        'prix_promo': 13500.00,
        'pourcentage_reduction': 10,
        'stock': 5,
        'est_disponible': True,
        'est_en_vedette': True,
        'categorie_slug': 'laptops'
    },
    {
        'id': 2,
        'nom': 'Apple MacBook Pro 14" M3',
        'slug': 'apple-macbook-pro-14-m3',
        'marque': 'Apple',
        'reference': 'MBP-M3-456',
        'description': 'Le MacBook Pro 14 pouces intègre la puce M3, offrant une vitesse et une efficacité énergétique exceptionnelles. Autonomie record jusqu\'à 22 heures, superbe écran Liquid Retina XDR de 14,2 pouces et design ultra-fin en aluminium. 8 Go de mémoire unifiée et 512 Go de stockage SSD.',
        'description_courte': 'Puce Apple M3, 8Go RAM, 512Go SSD, Écran Liquid Retina XDR.',
        'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=60',
        'prix': 24000.00,
        'prix_promo': None,
        'pourcentage_reduction': 0,
        'stock': 3,
        'est_disponible': True,
        'est_en_vedette': True,
        'categorie_slug': 'laptops'
    },
    {
        'id': 3,
        'nom': 'Razer BlackWidow V4 Pro',
        'slug': 'razer-blackwidow-v4-pro',
        'marque': 'Razer',
        'reference': 'RZ-BWV4-123',
        'description': 'Clavier mécanique de jeu haut de gamme équipé de switches verts Razer tactiles et cliquants. Rétroéclairage Razer Chroma RGB par touche et sous le châssis, molette de commande multifonction et 8 touches macros dédiées. Repose-poignet magnétique en similicuir molletonné pour un confort ultime.',
        'description_courte': 'Clavier mécanique Gamer, Switchs verts, Rétroéclairage RGB Chroma.',
        'image': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60',
        'prix': 1200.00,
        'prix_promo': 999.00,
        'pourcentage_reduction': 17,
        'stock': 15,
        'est_disponible': True,
        'est_en_vedette': False,
        'categorie_slug': 'peripheriques'
    },
    {
        'id': 4,
        'nom': 'Souris Logitech G502 Hero',
        'slug': 'souris-logitech-g502-hero',
        'marque': 'Logitech',
        'reference': 'LOG-G502-H',
        'description': 'La souris gaming la plus vendue au monde. Dispose d\'un capteur optique HERO 25K de haute précision, de 11 boutons programmables, d\'un poids ajustable personnalisé (5 poids de 3,6g fournis) et d\'un éclairage RGB LIGHTSYNC entièrement personnalisable. Roulette de défilement débrayable ultra-rapide.',
        'description_courte': 'Capteur HERO 25K (25600 DPI), 11 boutons programmables, Poids ajustables.',
        'image': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500&auto=format&fit=crop&q=60',
        'prix': 700.00,
        'prix_promo': None,
        'pourcentage_reduction': 0,
        'stock': 25,
        'est_disponible': True,
        'est_en_vedette': True,
        'categorie_slug': 'peripheriques'
    },
    {
        'id': 5,
        'nom': 'AMD Ryzen 7 7800X3D Processor',
        'slug': 'amd-ryzen-7-7800x3d-processor',
        'marque': 'AMD',
        'reference': 'AMD-R7-7800X3D',
        'description': 'Le processeur ultime pour les jeux vidéo sur PC avec la technologie AMD 3D V-Cache. Il dispose de 8 cœurs physiques et 16 threads, d\'un cache L3 massif de 96 Mo et d\'une fréquence boost jusqu\'à 5.0 GHz sur socket AM5 (architecture Zen 4). Faible consommation d\'énergie et efficacité record.',
        'description_courte': 'Socket AM5, 8 Cores/16 Threads, 96Mo 3D V-Cache, Fréquence Boost 5.0GHz.',
        'image': 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500&auto=format&fit=crop&q=60',
        'prix': 4500.00,
        'prix_promo': None,
        'pourcentage_reduction': 0,
        'stock': 8,
        'est_disponible': True,
        'est_en_vedette': True,
        'categorie_slug': 'composants'
    },
    {
        'id': 6,
        'nom': 'MSI RTX 4070 Ti Gaming X Slim 12G',
        'slug': 'msi-rtx-4070-ti-gaming-x-slim-12g',
        'marque': 'MSI',
        'reference': 'MSI-4070TI-SLIM',
        'description': 'Carte graphique haut de gamme avec architecture NVIDIA Ada Lovelace et refroidissement TRI FROZR 3. Bénéficiez du Ray Tracing complet et de la technologie intelligente DLSS 3. Dispose de 12 Go de mémoire GDDR6X, de ventilateurs TORX FAN 5.0 et d\'un format compact Slim.',
        'description_courte': 'NVIDIA GeForce RTX 4070 Ti, 12Go GDDR6X, Refroidissement Tri Frozr 3.',
        'image': 'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=500&auto=format&fit=crop&q=60',
        'prix': 9500.00,
        'prix_promo': 8999.00,
        'pourcentage_reduction': 5,
        'stock': 4,
        'est_disponible': True,
        'est_en_vedette': True,
        'categorie_slug': 'composants'
    },
    {
        'id': 7,
        'nom': 'iPhone 15 Pro Max 256GB - Titane Noir',
        'slug': 'iphone-15-pro-max-256gb-titane-noir',
        'marque': 'Apple',
        'reference': 'IP15PM-256-BK',
        'description': 'Le premier iPhone avec un design en titane de qualité aérospatiale, intégrant la surpuissante puce A17 Pro. Écran Super Retina XDR Always-On de 6,7 pouces, système photo de pointe avec zoom optique x5, et nouveau bouton Action personnalisable. Connectivité USB-C à haute vitesse.',
        'description_courte': 'Écran Super Retina XDR 6.7", Puce A17 Pro, 256Go de stockage.',
        'image': 'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=500&auto=format&fit=crop&q=60',
        'prix': 16000.00,
        'prix_promo': None,
        'pourcentage_reduction': 0,
        'stock': 0, # En rupture de stock !
        'est_disponible': False,
        'est_en_vedette': False,
        'categorie_slug': 'telephones'
    },
    {
        'id': 8,
        'nom': 'Samsung Galaxy S24 Ultra 512GB',
        'slug': 'samsung-galaxy-s24-ultra-512gb',
        'marque': 'Samsung',
        'reference': 'S24U-512-TI',
        'description': 'Découvrez le pouvoir de la Galaxy AI. Un cadre robuste en titane entoure un somptueux écran Dynamic AMOLED 2X de 6,8 pouces avec protection anti-reflets Gorilla Armor. Équipé du stylet S Pen intégré, d\'un processeur Snapdragon 8 Gen 3 et d\'un capteur photo exceptionnel de 200 Mpx.',
        'description_courte': 'Galaxy AI, Écran 6.8", Snapdragon 8 Gen 3, S Pen, Capteur photo 200Mpx.',
        'image': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500&auto=format&fit=crop&q=60',
        'prix': 14500.00,
        'prix_promo': 13200.00,
        'pourcentage_reduction': 9,
        'stock': 6,
        'est_disponible': True,
        'est_en_vedette': True,
        'categorie_slug': 'telephones'
    },
    {
        'id': 9,
        'nom': 'SSD Samsung 990 Pro M.2 NVMe 2To',
        'slug': 'ssd-samsung-990-pro-m2-nvme-2to',
        'marque': 'Samsung',
        'reference': 'SSD-SAM-990P-2T',
        'description': 'Atteignez des vitesses d\'écriture et de lecture quasi maximales avec l\'interface PCIe 4.0. Le SSD 990 Pro fournit des vitesses de lecture séquentielle allant jusqu\'à 7450 Mo/s et d\'écriture jusqu\'à 6900 Mo/s. Idéal pour les configurations gaming exigeantes et le traitement de données lourdes.',
        'description_courte': 'Interface PCIe 4.0 NVMe, Lecture 7450 Mo/s, Écriture 6900 Mo/s.',
        'image': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&auto=format&fit=crop&q=60',
        'prix': 1800.00,
        'prix_promo': None,
        'pourcentage_reduction': 0,
        'stock': 12,
        'est_disponible': True,
        'est_en_vedette': False,
        'categorie_slug': 'composants'
    },
    {
        'id': 10,
        'nom': 'Écran Gamer MSI Optix G274QPF-QD',
        'slug': 'ecran-gamer-msi-optix-g274qpf-qd',
        'marque': 'MSI',
        'reference': 'MSI-OPT-27QHD',
        'description': 'Moniteur gaming de 27 pouces avec dalle Rapid IPS de résolution WQHD (2560 x 1440). Profitez d\'un taux de rafraîchissement fluide de 170Hz et d\'un temps de réponse ultra-rapide de 1ms GtG. La technologie Quantum Dot offre des couleurs éclatantes et une couverture colorimétrique extrêmement riche.',
        'description_courte': 'Rapid IPS 27" WQHD, 170Hz, 1ms, Quantum Dot, compatible G-Sync.',
        'image': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&auto=format&fit=crop&q=60',
        'prix': 3200.00,
        'prix_promo': None,
        'pourcentage_reduction': 0,
        'stock': 7,
        'est_disponible': True,
        'est_en_vedette': True,
        'categorie_slug': 'peripheriques'
    }
]

# Helper to add dynamic attributes to mock products
def process_products(products_list):
    processed = []
    for prod in products_list:
        p = prod.copy()
        p['prix_effectif'] = p['prix_promo'] if p['prix_promo'] else p['prix']
        p['est_en_promo'] = p['prix_promo'] is not None
        p['reduction_mad'] = p['prix'] - p['prix_promo'] if p['prix_promo'] else 0
        processed.append(p)
    return processed

def get_processed_products():
    try:
        from apps.catalogue.models import Produit
        db_prods = list(Produit.objects.all())
        if db_prods:
            processed = []
            for p in db_prods:
                mock_p = next((mp for mp in PRODUITS if mp['id'] == p.id), None)
                img_url = mock_p['image'] if (mock_p and mock_p['image']) else ""
                if p.image:
                    img_url = p.image.url
                processed.append({
    'id': p.id,
    'db_obj': p,   
    'nom': p.nom,
    'slug': p.slug,
    'marque': p.marque,
    'reference': p.reference,
    'description': p.description,
    'description_courte': p.description_courte,
    'image': img_url,
    'prix': float(p.prix),
    'prix_promo': float(p.prix_promo) if p.prix_promo else None,
    'pourcentage_reduction': p.pourcentage_reduction,
    'stock': p.stock,
    'est_disponible': p.est_disponible,
    'est_en_vedette': p.est_en_vedette,
    'categorie_slug': p.categorie.slug,
    'prix_effectif': float(p.prix_effectif),
    'est_en_promo': p.est_en_promo,
    'reduction_mad': float(p.prix - p.prix_promo) if p.prix_promo else 0.0,
})
            return processed
    except Exception:
        pass
    return process_products(PRODUITS)

def accueil(request):
    processed_prods = get_processed_products()

    vedettes = [p for p in processed_prods if p['est_en_vedette']][:8]
    nouveautes = list(reversed(processed_prods))[:8]

    context = {
        'categories': Categorie.objects.filter(est_active=True),
        'produits_vedette': vedettes,
        'nouveautes': nouveautes,
        'marques': Produit.objects.values_list('marque', flat=True).distinct(),
    }

    return render(request, 'catalogue/accueil.html', context)

def liste_produits(request):
    processed_prods = get_processed_products()

    top = request.GET.get('top')

    if top:
        print("TOP =", top)

        for p in processed_prods:
            print(p["nom"], "=>", p["est_en_vedette"])

        processed_prods = [
            p for p in processed_prods
            if p["est_en_vedette"] is True
        ]

        print("Après filtre :", len(processed_prods))

    marque = request.GET.get('marque')
    if marque:
        processed_prods = [
            p for p in processed_prods
            if p['marque'].lower() == marque.lower()
        ]

    tri = request.GET.get('tri', 'recent')

    if tri == 'prix_asc':
        processed_prods.sort(key=lambda x: x['prix_effectif'])
    elif tri == 'prix_desc':
        processed_prods.sort(key=lambda x: x['prix_effectif'], reverse=True)
    elif tri == 'nom':
        processed_prods.sort(key=lambda x: x['nom'])

    context = {
        'produits': processed_prods,
        'categories': Categorie.objects.filter(est_active=True),
        'tri_actif': tri,
        'marques': Produit.objects.values_list('marque', flat=True).distinct(),
    }

    return render(request, 'catalogue/liste_produits.html', context)

from django.shortcuts import get_object_or_404

def liste_categorie(request, slug):
    processed_prods = get_processed_products()

    categorie = get_object_or_404(
        Categorie,
        slug=slug,
        est_active=True
    )

    filtres = [
        p for p in processed_prods
        if p['categorie_slug'] == slug
    ]

    tri = request.GET.get('tri', 'recent')

    if tri == 'prix_asc':
        filtres.sort(key=lambda x: x['prix_effectif'])
    elif tri == 'prix_desc':
        filtres.sort(key=lambda x: x['prix_effectif'], reverse=True)
    elif tri == 'nom':
        filtres.sort(key=lambda x: x['nom'])

    return render(request, "catalogue/liste_produits.html", {
        "categorie": categorie,
        "produits": filtres,
        "categories": Categorie.objects.filter(est_active=True),
        "tri_actif": tri,
    })

def detail_produit(request, id, slug):

    produit = get_object_or_404(
        Produit,
        id=id,
        slug=slug
    )

    print("=" * 50)
    print("Nom :", produit.nom)
    print("Image :", produit.image)
    print("URL :", produit.image.url if produit.image else "Aucune image")
    print("Nombre images :", produit.images.count())
    print("=" * 50)

    ...

    similaires = Produit.objects.filter(
        categorie=produit.categorie
    ).exclude(id=produit.id)[:4]

    produits_similaires = []

    for p in similaires:

        produits_similaires.append({
            'id': p.id,
            'nom': p.nom,
            'slug': p.slug,
            'marque': p.marque,
            'reference': p.reference,
            'description': p.description,
            'description_courte': p.description_courte,
            'image': p.image.url if p.image else "",
            'prix': float(p.prix),
            'prix_promo': float(p.prix_promo) if p.prix_promo else None,
            'pourcentage_reduction': p.pourcentage_reduction,
            'stock': p.stock,
            'est_disponible': p.est_disponible,
            'est_en_vedette': p.est_en_vedette,
            'categorie_slug': p.categorie.slug,
            'prix_effectif': float(p.prix_effectif),
            'est_en_promo': p.est_en_promo,
            'reduction_mad': float(p.prix - p.prix_promo) if p.prix_promo else 0,
        })

    return render(request, "catalogue/detail_produit.html", {
        "produit": produit,
        "produits_similaires": produits_similaires,
    })

def recherche(request):
    processed_prods = get_processed_products()
    query = request.GET.get('q', '').strip()

    if query:
        resultats = [
            p for p in processed_prods
            if query.lower() in p['nom'].lower()
            or query.lower() in p['marque'].lower()
            or query.lower() in p['reference'].lower()
            or query.lower() in p['description'].lower()
        ]
    else:
        resultats = []

    context = {
        'query': query,
        'produits': resultats,
        'categories': Categorie.objects.filter(est_active=True),
        'marques': Produit.objects.values_list('marque', flat=True).distinct(),
    }

    return render(request, 'catalogue/recherche.html', context)


def devis(request):
    context = {
        'categories': Categorie.objects.filter(est_active=True),
        'marques': Produit.objects.values_list('marque', flat=True).distinct(),
    }
    return render(request, 'catalogue/devis.html', context)


def contact_view(request):
    context = {
        'categories': Categorie.objects.filter(est_active=True),
        'marques': Produit.objects.values_list('marque', flat=True).distinct(),
    }
    return render(request, 'catalogue/contact.html', context)