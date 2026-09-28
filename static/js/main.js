// JavaScript pour InnovaTech

document.addEventListener("DOMContentLoaded", () => {

    // ==========================
    // 1. Auto-fermeture des alertes
    // ==========================
    const alerts = document.querySelectorAll(".alert-dismissible");

    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 4000);
    });

    // ==========================
    // 2. Boutons quantité +/-
    // ==========================
    const quantitySelectors = document.querySelectorAll(".quantity-selector");

    quantitySelectors.forEach(selector => {

        const minusBtn = selector.querySelector(".btn-qty-minus");
        const plusBtn = selector.querySelector(".btn-qty-plus");
        const input = selector.querySelector(".input-qty");

        if (minusBtn && plusBtn && input) {

            minusBtn.addEventListener("click", e => {

                e.preventDefault();

                let val = parseInt(input.value) || 1;

                if (val > 1) {
                    input.value = val - 1;
                    input.dispatchEvent(new Event("change", { bubbles: true }));
                }

            });

            plusBtn.addEventListener("click", e => {

                e.preventDefault();

                let val = parseInt(input.value) || 1;
                let max = parseInt(input.getAttribute("max")) || Infinity;

                if (val < max) {
                    input.value = val + 1;
                    input.dispatchEvent(new Event("change", { bubbles: true }));
                }

            });

        }

    });

    // ==========================
    // 3. Prévisualisation Avatar
    // ==========================
    const avatarInput = document.getElementById("avatar-input");
    const avatarPreview = document.getElementById("avatar-preview");

    if (avatarInput && avatarPreview) {

        avatarInput.addEventListener("change", function () {

            const file = this.files[0];

            if (file) {

                const reader = new FileReader();

                reader.onload = function (e) {
                    avatarPreview.src = e.target.result;
                };

                reader.readAsDataURL(file);

            }

        });

    }

    // ==========================
    // 4. Galerie Produit
    // ==========================
    const mainImg = document.getElementById("product-main-img");
    const thumbnails = document.querySelectorAll(".detail-thumb");

    thumbnails.forEach(thumb => {

        thumb.addEventListener("click", function () {

            if (mainImg) {

                mainImg.src = this.src;

                thumbnails.forEach(t => t.classList.remove("active"));

                this.classList.add("active");

            }

        });

    });

    // ==========================
    // 5. Mode Sombre
    // ==========================
    const themeToggle = document.getElementById("themeToggle");
    const themeText = document.getElementById("themeText");

    if (themeToggle) {

        function updateTheme() {

            const dark = document.body.classList.contains("dark-mode");

            themeToggle.checked = dark;

            if (themeText) {

                themeText.innerHTML = dark
                    ? "🌙 Mode sombre"
                    : "☀️ Mode clair";

            }

            localStorage.setItem("theme", dark ? "dark" : "light");

        }

        if (localStorage.getItem("theme") === "dark") {
            document.body.classList.add("dark-mode");
        }

        updateTheme();

        themeToggle.addEventListener("change", function () {

            document.body.classList.toggle("dark-mode", this.checked);

            updateTheme();

        });

    }

    // ==========================
    // 6. Wishlist AJAX
    // ==========================
    document.querySelectorAll(".wishlist-btn").forEach(btn => {

        btn.addEventListener("click", function (e) {

            e.preventDefault();

            fetch(this.dataset.url, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then(response => response.json())
                .then(data => {

                    const icon = this.querySelector("i");

                    if (data.status === "added") {

                        this.classList.add("active");

                        icon.classList.remove("bi-heart");

                        icon.classList.add("bi-heart-fill");

                    } else {

                        this.classList.remove("active");

                        icon.classList.remove("bi-heart-fill");

                        icon.classList.add("bi-heart");

                    }

                });

        });

    });

    // ==========================
    // 7. Ajout au Panier AJAX (sans redirection)
    // ==========================
    document.addEventListener("submit", function (e) {
        const form = e.target;
        if (form && form.action && form.action.includes("/panier/ajouter/")) {
            e.preventDefault();

            const formData = new FormData(form);
            const submitBtn = form.querySelector("button[type='submit'], .btn-add-cart, button");
            let originalText = "";
            if (submitBtn) {
                originalText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Ajout...`;
            }

            fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Mettre à jour le badge du panier dans le header
                    document.querySelectorAll(".action-badge, .cart-badge").forEach(badge => {
                        badge.textContent = data.total_items;
                    });

                    // Toast notification
                    showToastNotification(data.message, "success");

                    if (submitBtn) {
                        submitBtn.innerHTML = `<i class="bi bi-check2 me-1"></i> Ajouté !`;
                        submitBtn.classList.add("btn-success");
                        setTimeout(() => {
                            submitBtn.innerHTML = originalText;
                            submitBtn.classList.remove("btn-success");
                            submitBtn.disabled = false;
                        }, 2000);
                    }
                } else {
                    showToastNotification(data.message || "Erreur lors de l'ajout", "danger");
                    if (submitBtn) {
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }
                }
            })
            .catch(error => {
                console.error("Erreur panier:", error);
                showToastNotification("Une erreur s'est produite lors de l'ajout.", "danger");
                if (submitBtn) {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            });
        }
    });

    function showToastNotification(message, type = "success") {
        let container = document.getElementById("toast-notification-container");
        if (!container) {
            container = document.createElement("div");
            container.id = "toast-notification-container";
            container.className = "position-fixed bottom-0 end-0 p-3";
            container.style.zIndex = "1090";
            document.body.appendChild(container);
        }

        const toastEl = document.createElement("div");
        toastEl.className = `toast align-items-center text-white bg-${type === 'success' ? 'dark' : 'danger'} border-0 show shadow-lg mb-2`;
        toastEl.setAttribute("role", "alert");
        toastEl.setAttribute("aria-live", "assertive");
        toastEl.setAttribute("aria-atomic", "true");
        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body d-flex align-items-center gap-2">
                    <i class="bi ${type === 'success' ? 'bi-check-circle-fill text-warning' : 'bi-exclamation-triangle-fill'} fs-5"></i>
                    <span>${message}</span>
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        container.appendChild(toastEl);

        setTimeout(() => {
            toastEl.classList.remove("show");
            setTimeout(() => toastEl.remove(), 400);
        }, 3500);
    }

});