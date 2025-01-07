# API-s-curis-DJANGO-Et-Swagger-
Api sécurisé  conçu pour la communication avec la base de donnée de l'application Frontend Gestion des Rendez-vous de réparations d'automobiles 
# API Sécurisée - Gestion des Rendez-vous de Réparations Automobiles 🚗🔧

## Description
Cette API Django sécurisée est conçue pour interagir avec la base de données de l'application **Frontend - Gestion des Rendez-vous de Réparations Automobiles**. Elle permet la gestion des rendez-vous, des véhicules, des profils utilisateurs, et des mécaniciens via des endpoints RESTful sécurisés. L'API inclut également une documentation interactive grâce à **Swagger**.

## Fonctionnalités
- **Gestion des utilisateurs** : Inscription, connexion, et gestion des profils pour les clients et les mécaniciens.
- **Gestion des véhicules** : Ajouter, modifier, et consulter des informations sur les véhicules des clients.
- **Gestion des rendez-vous** : Planification, modification, et consultation des rendez-vous de réparation.
- **Authentification sécurisée** : Utilisation de **JWT (JSON Web Tokens)** pour sécuriser les accès à l'API.
- **Swagger UI** : Documentation interactive pour tester et explorer facilement l'API.

## Technologies utilisées
- **Django** : Framework Python pour la création de l'API backend.
- **Django Rest Framework (DRF)** : Pour la création de l'API RESTful.
- **Django REST Framework JWT** : Pour gérer l'authentification via JSON Web Tokens.
- **Swagger** : Pour la documentation interactive de l'API.
- **PostgreSQL / MySQL / SQLite** : Base de données relationnelle utilisée pour stocker les données.
  
## Endpoints principaux
- **POST /api/register/** : Créer un nouvel utilisateur.
- **POST /api/login/** : Connexion avec les informations d'identification (email et mot de passe).
- **GET /api/appointments/** : Récupérer tous les rendez-vous de réparation.
- **POST /api/appointments/** : Planifier un nouveau rendez-vous.
- **GET /api/vehicles/** : Récupérer les véhicules associés à l'utilisateur.
- **POST /api/vehicles/** : Ajouter un nouveau véhicule à l'utilisateur.

## Installation et configuration

### Prérequis
- Python 3.12 ou supérieur.
- Pip (gestionnaire de paquets Python).
- PostgreSQL / MySQL / SQLite (selon votre choix de base de données).

### Étapes d'installation
1. Clonez le dépôt sur votre machine locale :
   ```bash
   git clone https://github.com/oliveboss/API-s-curis-DJANGO-Et-Swagger.git
