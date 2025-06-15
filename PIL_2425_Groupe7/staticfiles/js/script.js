// script.js pour IFRI Comotorage

document.addEventListener('DOMContentLoaded', function() {
    console.log("Le script amélioré pour IFRI Comotorage est chargé ! Prêt pour l'aventure ?");

 
    AOS.init({
        duration: 800, 
        easing: 'ease-in-out-quad', 
        once: true, 
        offset: 50, 
    });

    // Optionnel : petit effet de décalage sur le titre de la section héros
    // pour un effet d'apparition plus dynamique si AOS n'est pas suffisant
    const titrePrincipal = document.querySelector('.titre-principal');
    if (titrePrincipal) {
        // Peut-être une animation de lettres ou de mots si souhaité
        // Par exemple, envelopper chaque mot dans un span et les animer
    }

    // Optionnel: smooth scroll pour les liens d'ancrage (si pas géré nativement par html { scroll-behavior: smooth; })
    const liensNav = document.querySelectorAll('.lien-navigation[href^="#"]');
    liensNav.forEach(lien => {
        lien.addEventListener('click', function(e) {
            e.preventDefault();
            let cibleID = this.getAttribute('href');
            let cibleElement = document.querySelector(cibleID);
            if (cibleElement) {
                // Ajustement pour la hauteur du header sticky
                let headerOffset = document.querySelector('.en-tete').offsetHeight || 70;
                let elementPosition = cibleElement.getBoundingClientRect().top;
                let offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });

                // Fermer le menu burger sur mobile après clic
                const navbarToggler = document.querySelector('.navbar-toggler');
                const navbarCollapse = document.querySelector('#navigationPrincipale');
                if (navbarToggler && !navbarToggler.classList.contains('collapsed')) {
                    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                         bootstrap.Collapse.getInstance(navbarCollapse).hide();
                    }
                }
            }
        });
    });


});