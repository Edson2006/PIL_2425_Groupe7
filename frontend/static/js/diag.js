// script.js

// Attend que le DOM soit entièrement chargé avant d'exécuter le script
// C'est une bonne pratique pour éviter les erreurs si le script est chargé avant les éléments HTML
document.addEventListener('DOMContentLoaded', () => {

    // --- SÉLECTION DES ÉLÉMENTS DU DOM ---
    const tousLesProcessus = document.querySelectorAll('.processus');
    const toutesLesBoites = document.querySelectorAll('.boite');
    const svgConnecteurs = document.querySelector('.connecteurs');
    
    // --- GESTION DE LA MODALE ---
    const modale = document.getElementById('modale');
    const btnFermer = document.querySelector('.modale-fermer');
    const modaleTitre = document.getElementById('modale-titre');
    const modaleDetailsP = document.getElementById('details-p');
    const modaleFluxEntrantsP = document.getElementById('flux-entrants-p');
    const modaleFluxSortantsP = document.getElementById('flux-sortants-p');

    // On associe à chaque processus une action au clic
    tousLesProcessus.forEach(processus => {
        processus.addEventListener('click', () => {
            // Récupération des informations stockées dans les attributs data-*
            const titre = processus.dataset.titre;
            const details = processus.dataset.details;
            const fluxEntrants = processus.dataset.fluxEntrants;
            const fluxSortants = processus.dataset.fluxSortants;

            // Remplissage de la modale avec ces informations
            modaleTitre.textContent = titre;
            modaleDetailsP.textContent = details;
            modaleFluxEntrantsP.textContent = fluxEntrants;
            modaleFluxSortantsP.textContent = fluxSortants;
            
            // Affichage de la modale
            modale.style.display = "block";
        });
    });

    // Action pour fermer la modale
    btnFermer.addEventListener('click', () => {
        modale.style.display = "none";
    });

    // Fermer la modale si on clique en dehors de son contenu
    window.addEventListener('click', (event) => {
        if (event.target == modale) {
            modale.style.display = "none";
        }
    });

    // --- DÉFINITION DES CONNEXIONS ET SURVOL ---
    
    // On définit ici les liens logiques entre les processus et les magasins de données
    // C'est un peu "en dur", mais pour un projet étudiant, c'est simple et efficace !
    const liens = {
        p1: ['utilisateur', 'd1'], // Gérer Compte -> Utilisateur & BDD Utilisateur
        p2: ['utilisateur', 'd2', 'd3', 'd4'], // Gérer Trajets -> Utilisateur & BDD Véhicules, Offres, Demandes
        p3: ['d3', 'd4', 'd5'], // Matching -> BDD Offres, Demandes, Matchings
        p4: ['utilisateur', 'd6'], // Messagerie -> Utilisateur & BDD Conversations
        p5: ['utilisateur', 'd1', 'd3', 'd4', 'd6'] // Tableau de bord -> toutes les données pertinentes
    };

    // Pour chaque processus, on ajoute les événements de survol
    tousLesProcessus.forEach(processus => {
        const idProcessus = processus.id;
        const ciblesLiees = liens[idProcessus] || [];

        processus.addEventListener('mouseover', () => {
            // On floute toutes les boîtes
            toutesLesBoites.forEach(b => b.classList.add('surbrillance-faible'));
            
            // On met en évidence le processus survolé et ses cibles
            processus.classList.remove('surbrillance-faible');
            processus.classList.add('surbrillance');

            ciblesLiees.forEach(idCible => {
                const cible = document.getElementById(idCible);
                if (cible) {
                    cible.classList.remove('surbrillance-faible');
                    cible.classList.add('surbrillance');
                }
            });

            // On met aussi en évidence les lignes de connexion
            document.querySelectorAll(`.connecteurs path[data-source="${idProcessus}"]`).forEach(path => {
                path.classList.add('surbrillance');
            });
        });

        processus.addEventListener('mouseout', () => {
            // On retire tous les effets de surbrillance
            toutesLesBoites.forEach(b => {
                b.classList.remove('surbrillance', 'surbrillance-faible');
            });
            document.querySelectorAll('.connecteurs path').forEach(path => {
                path.classList.remove('surbrillance');
            });
        });
    });


    // --- DESSIN DES LIGNES DE CONNEXION (Flux de données) ---

    // Fonction pour dessiner une ligne courbée entre deux éléments
    function dessinerLigne(idSource, idCible) {
        const source = document.getElementById(idSource);
        const cible = document.getElementById(idCible);

        if (!source || !cible) return;

        const rectSource = source.getBoundingClientRect();
        const rectCible = cible.getBoundingClientRect();
        const conteneurRect = svgConnecteurs.getBoundingClientRect();

        // Points de départ et d'arrivée relatifs au conteneur SVG
        const x1 = rectSource.right - conteneurRect.left;
        const y1 = rectSource.top + rectSource.height / 2 - conteneurRect.top;
        
        const x2 = rectCible.left - conteneurRect.left;
        const y2 = rectCible.top + rectCible.height / 2 - conteneurRect.top;

        // Création d'une courbe de Bézier pour un look plus "organique"
        const controleX = x1 + (x2 - x1) * 0.5;
        const chemin = `M ${x1} ${y1} C ${controleX} ${y1}, ${controleX} ${y2}, ${x2} ${y2}`;

        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', chemin);
        path.setAttribute('data-source', idSource);
        path.setAttribute('data-cible', idCible);
        
        // On ajoute une flèche à la fin de la ligne
        path.setAttribute('marker-end', 'url(#fleche)');

        svgConnecteurs.appendChild(path);
    }
    
    // Création de la définition de la flèche pour les lignes SVG
    function creerDefinitionFleche() {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
        marker.setAttribute('id', 'fleche');
        marker.setAttribute('viewBox', '0 0 10 10');
        marker.setAttribute('refX', '8');
        marker.setAttribute('refY', '5');
        marker.setAttribute('markerWidth', '6');
        marker.setAttribute('markerHeight', '6');
        marker.setAttribute('orient', 'auto-start-reverse');
        
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', 'M 0 0 L 10 5 L 0 10 z');
        path.style.fill = 'var(--couleur-flux)';
        
        marker.appendChild(path);
        defs.appendChild(marker);
        svgConnecteurs.appendChild(defs);
    }

    // Fonction pour dessiner toutes les connexions définies
    function dessinerToutesLesLignes() {
        // On vide les anciens connecteurs avant de redessiner
        svgConnecteurs.innerHTML = ''; 
        creerDefinitionFleche();

        for (const idProcessus in liens) {
            liens[idProcessus].forEach(idCible => {
                dessinerLigne(idProcessus, idCible);
                // On peut aussi dessiner le flux inverse (ex: de la BDD vers le processus)
                dessinerLigne(idCible, idProcessus);
            });
        }
    }

    // On s'assure que les polices sont chargées avant de dessiner les lignes pour un calcul de position correct
    document.fonts.ready.then(() => {
         // On attend un court instant que le layout soit stable
        setTimeout(dessinerToutesLesLignes, 100);
    });

    // On redessine les lignes si la fenêtre est redimensionnée
    window.addEventListener('resize', dessinerToutesLesLignes);
});