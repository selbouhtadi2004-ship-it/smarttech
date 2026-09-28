from django.core.management.base import BaseCommand
from decimal import Decimal
import random

from apps.catalogue.models import Produit, Categorie


class Command(BaseCommand):
    help = "Ajouter 300+ produits de démonstration"

    def handle(self, *args, **kwargs):

        def cat(slug):
            return Categorie.objects.get(slug=slug)

        # ==========================================
        # PARTIE 1 : LAPTOPS
        # ==========================================

        laptops = [
            ("ASUS ROG Strix G16","ASUS"),
            ("ASUS TUF Gaming A15","ASUS"),
            ("ASUS Zenbook 14 OLED","ASUS"),
            ("ASUS Vivobook 15","ASUS"),
            ("ASUS ExpertBook B1","ASUS"),

            ("Lenovo Legion 5","Lenovo"),
            ("Lenovo LOQ 15","Lenovo"),
            ("Lenovo IdeaPad Slim 3","Lenovo"),
            ("Lenovo ThinkPad E14","Lenovo"),
            ("Lenovo Yoga 7","Lenovo"),

            ("HP Victus 15","HP"),
            ("HP Omen 16","HP"),
            ("HP Pavilion 15","HP"),
            ("HP ProBook 450","HP"),
            ("HP EliteBook 840","HP"),

            ("Dell G15","Dell"),
            ("Dell Inspiron 15","Dell"),
            ("Dell XPS 13","Dell"),
            ("Dell Latitude 5440","Dell"),
            ("Dell Vostro 3520","Dell"),

            ("MSI Katana 15","MSI"),
            ("MSI Cyborg 15","MSI"),
            ("MSI Thin GF63","MSI"),
            ("MSI Stealth 16","MSI"),
            ("MSI Raider GE78","MSI"),

            ("Acer Nitro V15","Acer"),
            ("Acer Predator Helios Neo","Acer"),
            ("Acer Aspire 5","Acer"),
            ("Acer Swift Go 14","Acer"),
            ("Acer TravelMate P2","Acer"),

            ("Apple MacBook Air M2","Apple"),
            ("Apple MacBook Air M3","Apple"),
            ("Apple MacBook Pro 14 M4","Apple"),
            ("Apple MacBook Pro 16 M4","Apple"),
            ("Apple MacBook Air 15","Apple"),
        ]

        references = set()

        for i, (nom, marque) in enumerate(laptops, start=1):

            ref = f"LAP-{1000+i}"

            if ref in references:
                continue

            references.add(ref)

            prix = random.randint(6000, 35000)

            if random.choice([True, False]):
                prix_promo = Decimal(prix - random.randint(300, 2500))
            else:
                prix_promo = None

            Produit.objects.get_or_create(
                reference=ref,
                defaults={
                    "categorie": cat("laptops"),
                    "nom": nom,
                    "marque": marque,
                    "description": f"{nom} est un ordinateur portable performant adapté au gaming, au travail et aux études.",
                    "description_courte": nom,
                    "prix": Decimal(prix),
                    "prix_promo": prix_promo,
                    "stock": random.randint(3, 40),
                    "est_disponible": True,
                    "est_en_vedette": random.choice([True, False]),
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Partie 1 terminée : Laptops ajoutés."))
                # ==========================================
        # PARTIE 2 : PÉRIPHÉRIQUES
        # ==========================================

        peripheriques = [

            ("Logitech G502 HERO","Logitech"),
            ("Logitech G Pro X Superlight","Logitech"),
            ("Logitech MX Master 3S","Logitech"),
            ("Logitech MX Keys S","Logitech"),
            ("Logitech K380","Logitech"),
            ("Logitech G213","Logitech"),
            ("Logitech G733","Logitech"),
            ("Logitech C920 HD Webcam","Logitech"),
            ("Logitech Brio 4K","Logitech"),
            ("Logitech Z407 Speakers","Logitech"),

            ("Razer DeathAdder V3","Razer"),
            ("Razer Basilisk V3","Razer"),
            ("Razer BlackWidow V4","Razer"),
            ("Razer Huntsman Mini","Razer"),
            ("Razer Kraken X","Razer"),
            ("Razer Barracuda X","Razer"),
            ("Razer Kiyo Webcam","Razer"),
            ("Razer Gigantus V2","Razer"),

            ("Corsair K70 RGB","Corsair"),
            ("Corsair K55 RGB","Corsair"),
            ("Corsair M65 RGB","Corsair"),
            ("Corsair HS80","Corsair"),
            ("Corsair MM300 Mouse Pad","Corsair"),
            ("Corsair ST100 Headset Stand","Corsair"),

            ("HyperX Cloud II","HyperX"),
            ("HyperX Cloud III","HyperX"),
            ("HyperX Alloy Origins","HyperX"),
            ("HyperX Pulsefire Haste","HyperX"),
            ("HyperX QuadCast","HyperX"),

            ("SteelSeries Apex 3","SteelSeries"),
            ("SteelSeries Apex Pro","SteelSeries"),
            ("SteelSeries Rival 3","SteelSeries"),
            ("SteelSeries Arctis Nova 5","SteelSeries"),
            ("SteelSeries QcK Mouse Pad","SteelSeries"),

            ("ASUS ROG Chakram X","ASUS"),
            ("ASUS ROG Falchion","ASUS"),
            ("ASUS ROG Delta","ASUS"),
            ("ASUS ROG Eye Webcam","ASUS"),

            ("HP Wireless Mouse 220","HP"),
            ("HP USB Keyboard","HP"),
            ("HP Pavilion Webcam","HP"),
            ("HP Stereo Headset","HP"),

            ("Dell KM5221W","Dell"),
            ("Dell MS116 Mouse","Dell"),
            ("Dell Pro Webcam","Dell"),
            ("Dell Stereo Headset","Dell"),

            ("Samsung T7 SSD 1TB","Samsung"),
            ("Samsung T9 SSD 2TB","Samsung"),
            ("Samsung Smart Monitor M5","Samsung"),
            ("Samsung Odyssey G5","Samsung"),

            ("Xiaomi Wireless Mouse Lite","Xiaomi"),
            ("Xiaomi Monitor A24i","Xiaomi"),
            ("Xiaomi Redmi Buds 6","Xiaomi"),
        ]

        for i, (nom, marque) in enumerate(peripheriques, start=1):

            Produit.objects.get_or_create(
                reference=f"PER-{2000+i}",
                defaults={
                    "categorie": cat("peripheriques"),
                    "nom": nom,
                    "marque": marque,
                    "description": f"{nom} - Produit original {marque}.",
                    "description_courte": nom,
                    "prix": Decimal(random.randint(99, 4999)),
                    "prix_promo": None,
                    "stock": random.randint(5, 80),
                    "est_disponible": True,
                    "est_en_vedette": random.choice([True, False]),
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Partie 2 terminée : Périphériques ajoutés."))
                # ==========================================
        # PARTIE 3 : COMPOSANTS
        # ==========================================

        composants = [

            ("Intel Core i5-14400F", "Intel"),
            ("Intel Core i7-14700K", "Intel"),
            ("Intel Core i9-14900K", "Intel"),

            ("AMD Ryzen 5 7600", "AMD"),
            ("AMD Ryzen 7 7800X3D", "AMD"),
            ("AMD Ryzen 9 9950X", "AMD"),

            ("NVIDIA GeForce RTX 4060", "MSI"),
            ("NVIDIA GeForce RTX 4070 SUPER", "ASUS"),
            ("NVIDIA GeForce RTX 4080 SUPER", "Gigabyte"),
            ("NVIDIA GeForce RTX 4090", "MSI"),

            ("AMD Radeon RX 7700 XT", "Sapphire"),
            ("AMD Radeon RX 7800 XT", "XFX"),
            ("AMD Radeon RX 7900 XTX", "PowerColor"),

            ("Kingston Fury 16GB DDR5", "Kingston"),
            ("Kingston Fury 32GB DDR5", "Kingston"),
            ("Corsair Vengeance 32GB DDR5", "Corsair"),
            ("G.Skill Trident Z5 32GB", "G.Skill"),

            ("Samsung 990 PRO 1TB", "Samsung"),
            ("Samsung 990 PRO 2TB", "Samsung"),
            ("WD Black SN850X 1TB", "Western Digital"),
            ("Crucial P3 Plus 1TB", "Crucial"),

            ("MSI MAG B650 Tomahawk", "MSI"),
            ("ASUS ROG STRIX B650-A", "ASUS"),
            ("Gigabyte B760 Gaming X", "Gigabyte"),

            ("Corsair RM850x", "Corsair"),
            ("MSI MAG A750GL", "MSI"),
            ("Cooler Master MWE 750", "Cooler Master"),

            ("NZXT H5 Flow", "NZXT"),
            ("Lian Li Lancool 216", "Lian Li"),
            ("Corsair 4000D Airflow", "Corsair"),
        ]

        for i, (nom, marque) in enumerate(composants, start=1):

            Produit.objects.get_or_create(
                reference=f"CMP-{3000+i}",
                defaults={
                    "categorie": cat("composants"),
                    "nom": nom,
                    "marque": marque,
                    "description": f"{nom} - Composant informatique original {marque}.",
                    "description_courte": nom,
                    "prix": Decimal(random.randint(250, 18000)),
                    "prix_promo": None,
                    "stock": random.randint(4, 35),
                    "est_disponible": True,
                    "est_en_vedette": random.choice([True, False]),
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Partie 3 terminée : Composants ajoutés."))
                # ==========================================
        # PARTIE 4 : TÉLÉPHONES + RÉSEAU
        # ==========================================

        telephones = [

            ("iPhone 16", "Apple"),
            ("iPhone 16 Plus", "Apple"),
            ("iPhone 16 Pro", "Apple"),
            ("iPhone 16 Pro Max", "Apple"),

            ("Samsung Galaxy S25", "Samsung"),
            ("Samsung Galaxy S25+", "Samsung"),
            ("Samsung Galaxy S25 Ultra", "Samsung"),

            ("Xiaomi 15", "Xiaomi"),
            ("Xiaomi 15 Ultra", "Xiaomi"),
            ("Redmi Note 14 Pro", "Xiaomi"),

            ("Google Pixel 9", "Google"),
            ("Google Pixel 9 Pro", "Google"),

            ("OnePlus 13", "OnePlus"),
            ("Honor Magic7 Pro", "Honor"),
            ("Nothing Phone 3", "Nothing"),
        ]

        for i, (nom, marque) in enumerate(telephones, start=1):

            Produit.objects.get_or_create(
                reference=f"TEL-{4000+i}",
                defaults={
                    "categorie": cat("telephones"),
                    "nom": nom,
                    "marque": marque,
                    "description": f"{nom} Smartphone original {marque}.",
                    "description_courte": nom,
                    "prix": Decimal(random.randint(1800, 18000)),
                    "prix_promo": None,
                    "stock": random.randint(5, 60),
                    "est_disponible": True,
                    "est_en_vedette": random.choice([True, False]),
                }
            )

        reseau = [

            ("TP-Link Archer AX55", "TP-Link"),
            ("TP-Link Deco X20", "TP-Link"),
            ("TP-Link TL-SG108", "TP-Link"),

            ("D-Link DIR-X5460", "D-Link"),
            ("D-Link DGS-108", "D-Link"),

            ("ASUS RT-AX58U", "ASUS"),
            ("ASUS ZenWiFi XT8", "ASUS"),

            ("Ubiquiti UniFi U6+", "Ubiquiti"),
            ("Ubiquiti Dream Router", "Ubiquiti"),

            ("MikroTik hAP ax3", "MikroTik"),
            ("Cisco CBS110-8T-D", "Cisco"),
            ("Netgear Nighthawk AX6", "Netgear"),
        ]

        for i, (nom, marque) in enumerate(reseau, start=1):

            Produit.objects.get_or_create(
                reference=f"NET-{5000+i}",
                defaults={
                    "categorie": cat("reseau"),
                    "nom": nom,
                    "marque": marque,
                    "description": f"{nom} équipement réseau original {marque}.",
                    "description_courte": nom,
                    "prix": Decimal(random.randint(250, 6500)),
                    "prix_promo": None,
                    "stock": random.randint(3, 30),
                    "est_disponible": True,
                    "est_en_vedette": random.choice([True, False]),
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Partie 4 terminée : Téléphones + Réseau ajoutés."))