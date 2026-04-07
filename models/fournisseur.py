from db import execute_query


def get_all():
    return execute_query("SELECT id, nom, contact FROM fournisseurs ORDER BY nom", fetch=True)


def create(nom: str, contact: str):
    execute_query("INSERT INTO fournisseurs (nom, contact) VALUES (%s,%s)", (nom, contact))


def update(f_id: int, nom: str, contact: str):
    execute_query("UPDATE fournisseurs SET nom=%s, contact=%s WHERE id=%s", (nom, contact, f_id))


def delete(f_id: int):
    execute_query("DELETE FROM fournisseurs WHERE id=%s", (f_id,))
