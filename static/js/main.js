// JavaScript pour InnovaTech

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-fermeture des messages flash de notification après 4 secondes
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            // Utilise l'API Bootstrap 5 Alert
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 4000);
    });

    // 2. Boutons +/- pour la quantité sur la page détail produit et panier
    const quantitySelectors = document.querySelectorAll('.quantity-selector');
    quantitySelectors.forEach(selector => {
        const minusBtn = selector.querySelector('.btn-qty-minus');
        const plusBtn = selector.querySelector('.btn-qty-plus');
        const input = selector.querySelector('.input-qty');

        if (minusBtn && plusBtn && input) {
            minusBtn.addEventListener('click', (e) => {
                e.preventDefault();
                let val = parseInt(input.value) || 1;
                if (val > 1) {
                    input.value = val - 1;
                    // Déclenche l'événement change pour soumettre automatiquement le formulaire si nécessaire
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });

            plusBtn.addEventListener('click', (e) => {
                e.preventDefault();
                let val = parseInt(input.value) || 1;
                let max = parseInt(input.getAttribute('max')) || Infinity;
                if (val < max) {
                    input.value = val + 1;
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
        }
    });

    // 3. Aperçu image avatar sur la page profil (FileReader API)
    const avatarInput = document.getElementById('avatar-input');
    const avatarPreview = document.getElementById('avatar-preview');
    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    avatarPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // 4. Galerie photos sur la page détail produit
    const mainImg = document.getElementById('product-main-img');
    const thumbnails = document.querySelectorAll('.detail-thumb');
    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            if (mainImg) {
                mainImg.src = this.src;
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
});
