from db import execute_query


def get_all():
    return execute_query("SELECT id, nom FROM categories ORDER BY nom", fetch=True)


def create(nom: str):
    execute_query("INSERT INTO categories (nom) VALUES (%s)", (nom,))


def update(cat_id: int, nom: str):
    execute_query("UPDATE categories SET nom=%s WHERE id=%s", (nom, cat_id))


def delete(cat_id: int):
    execute_query("DELETE FROM categories WHERE id=%s", (cat_id,))
