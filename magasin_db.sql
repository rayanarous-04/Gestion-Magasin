"""
CREATE DATABASE IF NOT EXISTS magasin_db;
USE magasin_db;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE fournisseurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    contact VARCHAR(100)
);

CREATE TABLE produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prix FLOAT NOT NULL,
    quantite INT NOT NULL,
    categorie_id INT,
    fournisseur_id INT,
    FOREIGN KEY (categorie_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseurs(id) ON DELETE SET NULL
);

INSERT INTO categories (nom) VALUES ('Electronique'), ('Vêtements');
INSERT INTO fournisseurs (nom, contact) VALUES ('F1','123'), ('F2','456');
INSERT INTO produits (nom, prix, quantite, categorie_id, fournisseur_id)
VALUES ('PC', 2000, 5, 1, 1), ('T-shirt', 20, 50, 2, 2);
"""