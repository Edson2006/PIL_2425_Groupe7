document.addEventListener('DOMContentLoaded', () => {
    const elementsDFD = document.querySelectorAll('.entite-externe, .processus, .stockage-donnees');
    const infoPopup = document.getElementById('infoPopup');
    const popupTitre = document.getElementById('popupTitre');
    const popupTexte = document.getElementById('popupTexte');
    const fermerPopup = document.querySelector('.fermer-popup');

    elementsDFD.forEach(element => {
        element.addEventListener('click', () => {
            const nom = element.querySelector('.nom').textContent;
            const info = element.getAttribute('data-info');

            popupTitre.textContent = nom;
            popupTexte.textContent = info;
            infoPopup.style.display = 'flex';
        });
    });

    fermerPopup.addEventListener('click', () => {
        infoPopup.style.display = 'none';
    });

    // Close the popup if clicked outside of the content
    infoPopup.addEventListener('click', (event) => {
        if (event.target === infoPopup) {
            infoPopup.style.display = 'none';
        }
    });
});