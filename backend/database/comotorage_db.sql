-- =================================================================
-- Script de création de la base de données pour IFRI Covoiturage
-- Base de données : comotorag_db
-- =================================================================

-- Création de la base de données si elle n'existe pas
CREATE DATABASE IF NOT EXISTS comotorag_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Sélection de la base de données pour les commandes suivantes
USE comotorag_db;

-- =================================================================
-- Table 1: Utilisateur
-- Stocke les informations de base des utilisateurs.
-- =================================================================
CREATE TABLE IF NOT EXISTS Utilisateur (
    ID_Utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(50) NOT NULL,
    Prénom VARCHAR(50) NOT NULL,
    Numéro_de_Téléphone VARCHAR(15) NOT NULL UNIQUE,
    Adresse_E_mail VARCHAR(100) NOT NULL UNIQUE,
    Mot_de_Passe VARCHAR(255) NOT NULL,
    Rôle ENUM('Conducteur', 'Passager') NOT NULL,
    Photo_de_Profil VARCHAR(255) NULL
);

-- =================================================================
-- Table 2: Profil_Utilisateur
-- Stocke les préférences et informations complémentaires des utilisateurs.
-- Relation 1:1 avec Utilisateur.
-- =================================================================
CREATE TABLE IF NOT EXISTS Profil_Utilisateur (
    ID_Profil INT AUTO_INCREMENT PRIMARY KEY,
    ID_Utilisateur INT NOT NULL UNIQUE,
    Point_de_Départ TEXT NOT NULL,
    Horaires_de_Départ TIME NOT NULL,
    Horaires_d_Arrivée TIME NOT NULL,
    Marque VARCHAR(50) NULL,
    Modèle VARCHAR(50) NULL,
    Nombre_de_Places INT NULL CHECK (Nombre_de_Places > 0),
    FOREIGN KEY (ID_Utilisateur) REFERENCES Utilisateur(ID_Utilisateur) ON DELETE CASCADE
);

-- =================================================================
-- Table 3: Offres_de_Covoiturage
-- Stocke les offres publiées par les utilisateurs (conducteurs ou passagers).
-- =================================================================
CREATE TABLE IF NOT EXISTS Offres_de_Covoiturage (
    ID_Offre INT AUTO_INCREMENT PRIMARY KEY,
    ID_Utilisateur INT NOT NULL,
    Type ENUM('Conducteur', 'Passager') NOT NULL,
    Point_de_Départ_Offre TEXT NOT NULL,
    Point_d_Arrivée_Offre TEXT NOT NULL,
    Heure_de_Départ_Offre DATETIME NOT NULL,
    Nombre_de_Places_Offertes INT NULL CHECK (Nombre_de_Places_Offertes > 0),
    FOREIGN KEY (ID_Utilisateur) REFERENCES Utilisateur(ID_Utilisateur) ON DELETE CASCADE
);

-- =================================================================
-- Table 4: Demandes_de_Covoiturage
-- Stocke les demandes de trajet créées par les utilisateurs.
-- =================================================================
CREATE TABLE IF NOT EXISTS Demandes_de_Covoiturage (
    ID_Demande INT AUTO_INCREMENT PRIMARY KEY,
    ID_Utilisateur INT NOT NULL,
    Point_de_Départ_Demande TEXT NOT NULL,
    Point_d_Arrivée_Demande TEXT NOT NULL,
    Heure_de_Départ_Demande DATETIME NOT NULL,
    FOREIGN KEY (ID_Utilisateur) REFERENCES Utilisateur(ID_Utilisateur) ON DELETE CASCADE
);

-- =================================================================
-- Table 5: Correspondances
-- Table de liaison pour associer les offres et les demandes compatibles.
-- =================================================================
CREATE TABLE IF NOT EXISTS Correspondances (
    ID_Correspondance INT AUTO_INCREMENT PRIMARY KEY,
    ID_Offre INT NOT NULL,
    ID_Demande INT NOT NULL,
    Score_de_Correspondance DECIMAL(3,2) CHECK (Score_de_Correspondance BETWEEN 0.00 AND 1.00),
    FOREIGN KEY (ID_Offre) REFERENCES Offres_de_Covoiturage(ID_Offre) ON DELETE CASCADE,
    FOREIGN KEY (ID_Demande) REFERENCES Demandes_de_Covoiturage(ID_Demande) ON DELETE CASCADE
);

-- =================================================================
-- Table 6a: Conversations
-- Normalisation de l'entité Messagerie: stocke les conversations entre deux utilisateurs.
-- =================================================================
CREATE TABLE IF NOT EXISTS Conversations (
    ID_Conversation INT AUTO_INCREMENT PRIMARY KEY,
    ID_Utilisateur1 INT NOT NULL,
    ID_Utilisateur2 INT NOT NULL,
    FOREIGN KEY (ID_Utilisateur1) REFERENCES Utilisateur(ID_Utilisateur) ON DELETE CASCADE,
    FOREIGN KEY (ID_Utilisateur2) REFERENCES Utilisateur(ID_Utilisateur) ON DELETE CASCADE
);

-- =================================================================
-- Table 6b: Messages
-- Normalisation de l'entité Messagerie: stocke chaque message d'une conversation.
-- =================================================================
CREATE TABLE IF NOT EXISTS Messages (
    ID_Message INT AUTO_INCREMENT PRIMARY KEY,
    ID_Conversation INT NOT NULL,
    Expediteur INT NOT NULL,
    Contenu TEXT NOT NULL,
    Heure_d_Envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Conversation) REFERENCES Conversations(ID_Conversation) ON DELETE CASCADE,
    FOREIGN KEY (Expediteur) REFERENCES Utilisateur(ID_Utilisateur) ON DELETE CASCADE
);

-- =================================================================
-- Table 7: Notifications
-- Stocke les notifications envoyées aux utilisateurs.
-- =================================================================
CREATE TABLE IF NOT EXISTS Notifications (
    ID_Notification INT AUTO_INCREMENT PRIMARY KEY,
    ID_Utilisateur INT NOT NULL,
    Type_Notification ENUM('Message', 'Correspondance', 'Système') NOT NULL,
    Contenu VARCHAR(255) NOT NULL,
    Heure_d_Envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Lu BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (ID_Utilisateur) REFERENCES Utilisateur(ID_Utilisateur) ON DELETE CASCADE
);

-- =================================================================
-- Fin du script.
-- =================================================================