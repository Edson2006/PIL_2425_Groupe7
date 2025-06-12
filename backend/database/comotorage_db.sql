CREATE DATABASE IF NOT EXISTS covoiturage_db;
USE covoiturage_db;

-- Table utilisateurs
CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    telephone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    role ENUM('conducteur', 'passager') DEFAULT 'passager',
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table profils utilisateurs
CREATE TABLE profils_utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    photo_profil TEXT,
    point_depart TEXT,
    horaires_depart TIME,
    horaires_arrivee TIME,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table véhicules
CREATE TABLE vehicules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    marque VARCHAR(100),
    modele VARCHAR(100),
    nombre_places INT,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table offres de covoiturage
CREATE TABLE offres_covoiturage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conducteur_id INT NOT NULL,
    point_depart TEXT NOT NULL,
    point_arrivee TEXT NOT NULL,
    heure_depart DATETIME NOT NULL,
    places_disponibles INT NOT NULL,
    FOREIGN KEY (conducteur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table demandes de covoiturage
CREATE TABLE demandes_covoiturage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passager_id INT NOT NULL,
    point_depart TEXT NOT NULL,
    point_arrivee TEXT NOT NULL,
    heure_souhaitee DATETIME NOT NULL,
    FOREIGN KEY (passager_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table matchings (correspondances)
CREATE TABLE matchings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    offre_id INT NOT NULL,
    demande_id INT NOT NULL,
    score_match FLOAT,
    FOREIGN KEY (offre_id) REFERENCES offres_covoiturage(id) ON DELETE CASCADE,
    FOREIGN KEY (demande_id) REFERENCES demandes_covoiturage(id) ON DELETE CASCADE
);

-- Table conversations (entre deux utilisateurs)
CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur1_id INT NOT NULL,
    utilisateur2_id INT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur1_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (utilisateur2_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

-- Table messages
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    expediteur_id INT NOT NULL,
    contenu TEXT NOT NULL,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (expediteur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
);

DROP DATABASE IF EXISTS covoiturage_db;
CREATE DATABASE covoiturage_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
