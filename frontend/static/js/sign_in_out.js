
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