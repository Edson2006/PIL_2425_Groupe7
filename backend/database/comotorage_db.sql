-- =================================================================
-- Script de création de la base de données pour IFRI Covoiturage
-- Base de données : comotorag_db
-- =================================================================

-- Création de la base de données si elle n'existe pas
CREATE DATABASE IF NOT EXISTS comotorage_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Sélection de la base de données pour les commandes suivantes
USE comotorage_db;

-- =================================================================
-- Table 1: Utilisateur
-- Stocke les informations de base des utilisateurs.
-- =================================================================
-- Table des utilisateurs
CREATE TABLE utilisateurs (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    numero_telephone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    role ENUM('conducteur', 'passager') DEFAULT 'passager',
    photo_profil TEXT,
    point_depart_habituel TEXT,
    heure_depart_habituelle TIME,
    heure_arrivee_habituelle TIME,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des véhicules
CREATE TABLE vehicules (
    id_vehicule INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    marque VARCHAR(50) NOT NULL,
    modele VARCHAR(50) NOT NULL,
    nombre_places INT NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur)
);

-- Table des offres de covoiturage
CREATE TABLE offres_covoiturage (
    id_offre INT AUTO_INCREMENT PRIMARY KEY,
    id_conducteur INT NOT NULL,
    point_depart TEXT NOT NULL,
    point_arrivee TEXT NOT NULL,
    date_heure_depart DATETIME NOT NULL,
    places_disponibles INT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_conducteur) REFERENCES utilisateurs(id_utilisateur)
);

-- Table des demandes de covoiturage
CREATE TABLE demandes_covoiturage (
    id_demande INT AUTO_INCREMENT PRIMARY KEY,
    id_passager INT NOT NULL,
    point_depart TEXT NOT NULL,
    point_arrivee TEXT NOT NULL,
    date_heure_souhaitee DATETIME NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_passager) REFERENCES utilisateurs(id_utilisateur)
);

-- Table de correspondance conducteur/passager (matching)
CREATE TABLE correspondances (
    id_correspondance INT AUTO_INCREMENT PRIMARY KEY,
    id_offre INT NOT NULL,
    id_demande INT NOT NULL,
    taux_compatibilite FLOAT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_offre) REFERENCES offres_covoiturage(id_offre),
    FOREIGN KEY (id_demande) REFERENCES demandes_covoiturage(id_demande)
);

-- Table des conversations
CREATE TABLE conversations (
    id_conversation INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur_1 INT NOT NULL,
    id_utilisateur_2 INT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilisateur_1) REFERENCES utilisateurs(id_utilisateur),
    FOREIGN KEY (id_utilisateur_2) REFERENCES utilisateurs(id_utilisateur)
);

-- Table des messages
CREATE TABLE messages (
    id_message INT AUTO_INCREMENT PRIMARY KEY,
    id_conversation INT NOT NULL,
    id_expediteur INT NOT NULL,
    contenu TEXT NOT NULL,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lu BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_conversation) REFERENCES conversations(id_conversation),
    FOREIGN KEY (id_expediteur) REFERENCES utilisateurs(id_utilisateur)
);

-- Table des réinitialisations de mot de passe
CREATE TABLE reinitialisations_mot_de_passe (
    id_reinitialisation INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    token VARCHAR(255) NOT NULL UNIQUE,
    date_expiration TIMESTAMP NOT NULL,
    utilise BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur)
);
