# 🏪 Gestion Magasin Pro

Application desktop de gestion de stock développée en Python avec CustomTkinter et MySQL.

## Technologies

| Composant | Technologie |
|---|---|
| Langage | Python 3.10+ |
| Interface | CustomTkinter |
| Base de données | MySQL 8.x |
| Connecteur BDD | mysql-connector-python |

## Structure du projet

```
magasin/
├── main.py               # Point d'entrée de l'application
├── config.py             # Configuration DB et paramètres app
├── db.py                 # Couche d'accès à la base de données
├── magasin_db.sql        # Script SQL (tables + données de test)
├── models/
│   ├── produit.py        # Requêtes SQL produits
│   ├── categorie.py      # Requêtes SQL catégories
│   └── fournisseur.py    # Requêtes SQL fournisseurs
└── views/
    ├── base_view.py      # Composant Treeview réutilisable
    ├── produits_view.py  # Vue CRUD produits
    ├── categories_view.py
    └── fournisseurs_view.py
```

## Installation

### 1. Prérequis

- Python 3.10 ou supérieur
- MySQL 8.x (WAMP / XAMPP / MySQL Server)

### 2. Installer les dépendances

```bash
pip install mysql-connector-python customtkinter
```

### 3. Configurer la base de données

1. Démarrer votre serveur MySQL
2. Importer le script SQL :
```bash
mysql -u root -p < magasin_db.sql
```
Ou via phpMyAdmin : importer le fichier `magasin_db.sql`.

### 4. Configurer la connexion

Modifier `config.py` selon votre environnement :

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "votre_mot_de_passe",  # laisser vide si aucun
    "database": "magasin_db"
}
```

### 5. Lancer l'application

```bash
python main.py
```

## Fonctionnalités

- **Produits** : CRUD complet avec sélection de catégorie et fournisseur, statistiques, export CSV
- **Catégories** : CRUD complet
- **Fournisseurs** : CRUD complet
- **Recherche dynamique** sur tous les onglets
- **Tri des colonnes** au clic (ascendant / descendant)
- **Validation des saisies** avec messages d'erreur inline
- **Export CSV** avec encodage UTF-8
