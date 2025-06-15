
document.addEventListener('DOMContentLoaded', () => {

    
    const boutonInscription = document.getElementById('bouton-inscription');
    const boutonConnexion = document.getElementById('bouton-connexion');
    const conteneurPrincipal = document.getElementById('conteneur-principal');
    boutonInscription.addEventListener('click', () => {
       
        conteneurPrincipal.classList.add('mode-inscription-active');
    });
    boutonConnexion.addEventListener('click', () => {
        conteneurPrincipal.classList.remove('mode-inscription-active');
    });

});

document.addEventListener('DOMContentLoaded', function() {
    const conteneurPrincipal = document.getElementById('conteneur-principal');
    const boutonInscription = document.getElementById('bouton-inscription');
    const boutonConnexion = document.getElementById('bouton-connexion');
    
    // Vérifier si nous sommes sur la page d'inscription
    const urlParams = new URLSearchParams(window.location.search);
    const action = urlParams.get('action');
    
    if (action === 'register') {
        conteneurPrincipal.classList.add('active-inscription');
    }
    
    // Gestion des boutons
    boutonInscription.addEventListener('click', () => {
        conteneurPrincipal.classList.add('active-inscription');
        history.pushState(null, null, '?action=register');
    });
    
    boutonConnexion.addEventListener('click', () => {
        conteneurPrincipal.classList.remove('active-inscription');
        history.pushState(null, null, window.location.pathname);
    });
    
    // Effets de transition pour les inputs
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.zIndex = '10';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
            this.parentElement.style.zIndex = '1';
        });
    });
    
    // Animation du formulaire
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const spinner = submitBtn.querySelector('.fa-spinner');
            const text = submitBtn.querySelector('#register-text');
            
            if (spinner && text) {
                text.style.display = 'none';
                spinner.style.display = 'inline-block';
                submitBtn.disabled = true;
            }
        });
    });
});