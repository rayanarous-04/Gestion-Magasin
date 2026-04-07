from db import execute_query


def get_all():
    return execute_query(
        """SELECT p.id, p.nom, p.prix, p.quantite,
                  COALESCE(c.nom, '—') AS categorie,
                  COALESCE(f.nom, '—') AS fournisseur
           FROM produits p
           LEFT JOIN categories c ON p.categorie_id = c.id
           LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
           ORDER BY p.id""",
        fetch=True
    )


def search(keyword: str):
    return execute_query(
        """SELECT p.id, p.nom, p.prix, p.quantite,
                  COALESCE(c.nom, '—') AS categorie,
                  COALESCE(f.nom, '—') AS fournisseur
           FROM produits p
           LEFT JOIN categories c ON p.categorie_id = c.id
           LEFT JOIN fournisseurs f ON p.fournisseur_id = f.id
           WHERE p.nom LIKE %s OR c.nom LIKE %s OR f.nom LIKE %s""",
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        fetch=True
    )


def create(nom: str, prix: float, quantite: int,
           categorie_id: int | None, fournisseur_id: int | None):
    execute_query(
        "INSERT INTO produits (nom, prix, quantite, categorie_id, fournisseur_id) VALUES (%s,%s,%s,%s,%s)",
        (nom, prix, quantite, categorie_id, fournisseur_id)
    )


def update(product_id: int, nom: str, prix: float, quantite: int,
           categorie_id: int | None, fournisseur_id: int | None):
    execute_query(
        "UPDATE produits SET nom=%s, prix=%s, quantite=%s, categorie_id=%s, fournisseur_id=%s WHERE id=%s",
        (nom, prix, quantite, categorie_id, fournisseur_id, product_id)
    )


def delete(product_id: int):
    execute_query("DELETE FROM produits WHERE id=%s", (product_id,))


def get_stats():
    rows = execute_query(
        "SELECT COUNT(*), COALESCE(SUM(prix * quantite), 0), COALESCE(AVG(prix), 0) FROM produits",
        fetch=True
    )
    return rows[0] if rows else (0, 0, 0)
