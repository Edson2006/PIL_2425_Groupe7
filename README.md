# 🚗IFRI_COMOTORAGE: Plateforme de Covoiturage avec Django

Une application web robuste développée avec Django pour gérer une plateforme de mise en relation pour le covoiturage. Ce projet permet aux utilisateurs de proposer, rechercher et réserver des trajets simplement et efficacement.

---

## 📋 Table des matières

- [Description](#description)
- [Fonctionnalités clés](#fonctionnalités-clés)
- [Technologies utilisées](#technologies-utilisées)
- [Prérequis](#prérequis)
- [Installation et Lancement](#installation-et-lancement)
- [Contribuer](#contribuer)
- [Licence](#licence)

---

## 📝 Description

IFRI_COMOTORAGE est une solution complète pour créer une communauté de covoiturage. Elle met en relation des conducteurs disposant de places libres avec des passagers cherchant à effectuer le même trajet. L'application est conçue pour être simple, efficace et sécurisée, en s'appuyant sur la puissance du framework Django et une base de données MySQL.

---

## ✨ Fonctionnalités clés

### 👤 Gestion des Utilisateurs
- Inscription et authentification sécurisées
- Profils utilisateurs personnalisables
- Gestion de session (connexion / déconnexion)

### 🚗 Gestion des Trajets
- **Conducteurs** : Publication facile de nouveaux trajets (villes de départ/arrivée, date, heure, places, prix)
- **Passagers** : Recherche intuitive et filtrage des trajets disponibles
- Consultation des détails complets d'un trajet avant de réserver



### ⚙️ Interface d'Administration
- Interface d'administration Django intégrée pour une gestion centralisée des utilisateurs, trajets et réservations

---

## 🛠️ Technologies utilisées

- **Backend** : Python 3 / Django
- **Base de Données** : MySQL
- **Gestion des variables d'environnement** : python-decouple

---

## ✅ Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants sur votre machine :

- Python 3.8+ et son gestionnaire de paquets `pip`
- Git
- Un serveur de base de données MySQL fonctionnel

---

## 🚀 Installation et Lancement

Suivez ces étapes pour mettre en place le projet en local.

### 1. Cloner le Dépôt

```bash
git clone https://github.com/Edson2006/PIL_2425_Groupe7.git
cd PIL_2425_Groupe7
```

### 2. Créer et Activer un Environnement Virtuel

Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.

**Sur macOS/Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Sur Windows :**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la Base de Données

Créez une base de données dans votre serveur MySQL.

```sql
CREATE DATABASE covoiturage_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Créez un fichier `.env` à la racine du projet (au même niveau que `manage.py`). Copiez-y le contenu suivant et adaptez les valeurs à votre configuration MySQL.

```ini


SECRET_KEY='votre_clé_secrète_django_ici' # Générer une clé secrète unique pour votre environnement.
    Note : Pour générer une clé secrète, vous pouvez lancer en Python :```bash
        from django.core.management.utils import get_random_secret_key
         print(get_random_secret_key())
        ```
    puis copier la clé générée ici. 
DEBUG=True

DB_NAME=covoiturage_db
DB_USER=root
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=3306
```

> **Important** : Le fichier `.env` est ignoré par Git (via le `.gitignore`) pour protéger vos identifiants.

### 5. Lancer l'Application

Appliquez les migrations pour créer les tables dans la base de données.

```bash
python manage.py makemigrations
python manage.py migrate
```

Créez un super-utilisateur pour accéder à l'interface d'administration.

```bash
python manage.py createsuperuser
```
Suivez les instructions pour définir un nom d'utilisateur, une adresse e-mail et un mot de passe.

Démarrez le serveur de développement.

```bash
python manage.py runserver
```

Votre application est maintenant accessible à l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000).

L'interface d'administration est disponible sur [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

---
🐞 Note sur le débogage
    Pour faciliter la compréhension et le débogage du projet, nous avons ajouté des print() de debug à plusieurs endroits stratégiques du code.

    Ces messages s’affichent dans la console lors de l’exécution, ce qui permet de suivre le déroulement et de mieux diagnostiquer les éventuels problèmes.

    Cela peut aider grandement lors de la correction ou de la maintenance du projet.