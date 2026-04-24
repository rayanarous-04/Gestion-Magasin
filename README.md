# 🏪 Gestion Magasin Pro

> Application desktop de gestion de stock développée en Python avec CustomTkinter et MySQL.


---

## 📋 Description

Application de gestion de magasin permettant de gérer les **produits**, **catégories** et **fournisseurs** via une interface graphique moderne. Développée dans le cadre d'un projet semestriel de 1ère année ingénieur informatique.

---

## ✨ Fonctionnalités

- 🛒 **Gestion des produits** — Ajout, modification, suppression, affichage
- 🏷 **Gestion des catégories** — CRUD complet
- 🚚 **Gestion des fournisseurs** — CRUD complet
- 🔍 **Recherche dynamique** en temps réel sur tous les onglets
- 🔃 **Tri des colonnes** au clic (ascendant / descendant)
- 📊 **Statistiques** — nombre de produits, valeur totale du stock, prix moyen
- 📥 **Export CSV** compatible Excel (encodage UTF-8)
- ✅ **Validation des saisies** avec messages d'erreur inline
- 🌙 **Thème dark/light** configurable

---

## 🛠 Technologies

| Composant | Technologie |
|---|---|
| Langage | Python 3.10+ |
| Interface graphique | CustomTkinter |
| Base de données | MySQL 8.x |
| Connecteur BDD | mysql-connector-python |
| IDE recommandé | VS Code / PyCharm |

---

## 📁 Structure du projet

```
magasin/
├── main.py                  # Point d'entrée — fenêtre principale + navigation
├── config.py                # Configuration DB et paramètres application
├── db.py                    # Couche d'accès à la base de données
├── magasin_db.sql           # Script SQL (création tables + données de test)
├── README.md
├── models/
│   ├── produit.py           # Requêtes SQL produits
│   ├── categorie.py         # Requêtes SQL catégories
│   └── fournisseur.py       # Requêtes SQL fournisseurs
└── views/
    ├── base_view.py         # Composant Treeview réutilisable
    ├── produits_view.py     # Vue CRUD produits
    ├── categories_view.py   # Vue CRUD catégories
    └── fournisseurs_view.py # Vue CRUD fournisseurs
```

---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/TON_USERNAME/gestion-magasin.git
cd gestion-magasin
```

### 2. Installer les dépendances

```bash
pip install mysql-connector-python customtkinter
```

### 3. Configurer la base de données

Démarrez votre serveur MySQL (WAMP / XAMPP / MySQL Server), puis importez le script SQL :

```bash
mysql -u root -p < magasin_db.sql
```

Ou via **phpMyAdmin** : créer une base `magasin_db` → onglet *Importer* → sélectionner `magasin_db.sql`.

### 4. Configurer la connexion

Modifiez `config.py` selon votre environnement :

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",        # votre mot de passe MySQL
    "database": "magasin_db"
}
```

### 5. Lancer l'application

```bash
python main.py
```

---

## 📸 Aperçu

> *(Ajoutez ici une capture d'écran de l'application)*

---



---

## ⚙️ Configuration avancée

Le fichier `config.py` permet de personnaliser :

```python
THEME = "dark"         # "dark" ou "light"
COLOR_THEME = "blue"   # "blue", "green", "dark-blue"
APP_GEOMETRY = "1200x700"
```

---

## 📌 Prérequis système

- Python **3.10** ou supérieur
- MySQL **8.x**
- Windows / macOS / Linux

---

## 👤 Auteur

**Rayen Arous**  
Étudiant en 1ère année ingénieur informatique  
[GitHub](https://github.com/rayanarous-04)

---

## 📄 Licence

Ce projet est sous licence MIT.
